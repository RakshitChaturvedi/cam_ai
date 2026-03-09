import os
import json
import asyncio

# -- INGESTION IMPORTS --
from main import run_ingestion

# -- RESEARCH AGENT IMPORTS --
from research_agent.crawlers.payload_receiver import validate_payload
from research_agent.crawlers.query_architect import construct_queries
from research_agent.crawlers.engines import litigation, promoter, sector_risk
from research_agent.crawlers.data_normalizer import clean_and_tag

from research_agent.rag_pipeline.finmm_editor import correct_ocr_hallucinations
from research_agent.rag_pipeline.spatial_chunker import chunk_document
from research_agent.rag_pipeline.embedding_db import LocalVectorDB


async def integrated_test():
    print("=========================================================")
    print("      INTEGRATED E2E TEST: INGESTION -> CRAWLER -> RAG     ")
    print("=========================================================")
    
    # -------------------------------------------------------------
    # STAGE 1: DATA INGESTION
    # -------------------------------------------------------------
    print("\n>>> STAGE 1: RUNNING DATA INGESTION ON RAW PDFs/CSVs...")
    
    crawler_payload, original_payload = run_ingestion()
    
    print("\n[INGESTION OUTPUT] Payload 1 (Crawler Trigger):")
    print(json.dumps(crawler_payload, indent=2))
    print("\n[INGESTION OUTPUT] Payload 2 (Original Data - Truncated for display):")
    # Just print the keys/summary to avoid flooding console
    print(f"Unstructured Docs Processed: {list(original_payload['unstructured_signals'].keys())}")
    print(f"Structured Signals Risk Summary: {original_payload['structured_signals']['structured_financial_analysis']['risk_summary']}")
    
    
    # -------------------------------------------------------------
    # STAGE 2: CRAWLING 
    # -------------------------------------------------------------
    print("\n>>> STAGE 2: PASSING PAYLOAD TO CRAWLER LAYER...")
    
    is_valid, validation_data = validate_payload(crawler_payload)
    if not is_valid:
        print(f"Payload validation failed: {validation_data.get('error')}")
        return
        
    print(f"Needs LLM Fallback (Regex Check)? {validation_data['needs_llm_fallback']}")
    
    print("Constructing Queries...")
    queries_dict = construct_queries(validation_data)
    print(json.dumps(queries_dict, indent=2))
    
    print("\nExecuting Scrapers concurrently...")
    lit_task = litigation.run_litigation_scraper(
        query=queries_dict.get("litigation_query", ""), 
        entity_details=crawler_payload["entity_details"]
    )
    
    prom_task = promoter.run_promoter_scraper(
        query=queries_dict.get("promoter_query", ""), 
        promoters=crawler_payload["promoter_details"]
    )
    
    sec_task = sector_risk.run_sector_scraper(
        query=queries_dict.get("regulatory_query", ""), 
        temporal_context=crawler_payload["temporal_context"]
    )
    
    results = await asyncio.gather(lit_task, prom_task, sec_task)
    
    rag_objects = []
    
    for res in results:
        clean_obj = clean_and_tag(res)
        
        # Inject the parsed PAN to the metadata to show how they tie together
        clean_obj["metadata"]["entity_pan"] = crawler_payload.get("entity_details", {}).get("company_pan", "UNKNOWN")
        
        rag_objects.append(clean_obj)
        
    print("\n[CRAWLER OUTPUT] Cleaned & Tagged Output ready for RAG:")
    print(json.dumps(rag_objects, indent=2))
    
    
    # -------------------------------------------------------------
    # STAGE 3: RAG PIPELINE
    # -------------------------------------------------------------
    print("\n>>> STAGE 3: INGESTING INTO RAG FAISS DATABASE...")
    
    print("Initializing FAISS DB...")
    db = LocalVectorDB()
    
    all_chunks = []
    for ro in rag_objects:
        # OCR Correction Layer
        ro["content"] = correct_ocr_hallucinations(ro["content"])
        
        # Spatial Chunker (Preserve tables vs standard text)
        doc_chunks = chunk_document(ro)
        all_chunks.extend(doc_chunks)
        
    # Embedding DB (FAISS storage)
    db.add_chunks(all_chunks)
    
    print("\n[RAG PIPELINE] Successfully vectorized what the crawlers returned and stored it into FAISS!")
    print("\nIntegrated Test Complete. End-to-end chain is fully functional.")

if __name__ == "__main__":
    asyncio.run(integrated_test())
