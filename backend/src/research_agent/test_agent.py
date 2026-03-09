import json
import asyncio

# --- CRAWLER IMPORTS ---
from crawlers.payload_receiver import validate_payload
from crawlers.query_architect import construct_queries
from crawlers.engines import litigation, promoter, sector_risk
from crawlers.data_normalizer import clean_and_tag

# --- RAG PIPELINE IMPORTS ---
from rag_pipeline.finmm_editor import correct_ocr_hallucinations
from rag_pipeline.spatial_chunker import chunk_document
from rag_pipeline.embedding_db import LocalVectorDB
from rag_pipeline.modular_retriever import iterative_search
from rag_pipeline.refine_verifier import verify_findings


async def main():
    print("Initializing Local Vector DB (Downloading HuggingFace model if first run)...")
    db = LocalVectorDB()
    
    # -------------------------------------------------------------
    # STAGE 1: INGESTION (Mock Payload)
    # -------------------------------------------------------------
    crawler_payload = {
        "entity_details": {
            "company_name": "ABC Textiles Pvt Ltd",
            "company_pan": "ABCDE1234F", # Valid PAN to force hard-filtering
            "cin": "L12345MH2000PLC123456",
            "nic_code": "13",
            "pin_code": "400001"
        },
        "promoter_details": [
            {"name": "Rahul Sharma", "din": "12345678", "pan": "VWXYZ9876Q"}
        ],
        "temporal_context": {
            "target_fy": "FY 2023-2024",
            "start_date": "2023-04-01",
            "end_date": "2024-03-31"
        }
    }
    
    # -------------------------------------------------------------
    # STAGE 2: CRAWLING 
    # -------------------------------------------------------------
    print("\n--- [STAGE 2] CRAWLING ---")
    is_valid, validation_data = validate_payload(crawler_payload)
    queries_dict = construct_queries(validation_data)
    
    # Inject an intentional OCR typo into our simulated scrape result 
    # to prove the `finmm_editor` works (? 50,000 should become ₹ 50,000)
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
        # Intentionally pollute the raw text for our demonstration
        if res["engine"] == "litigation":
            res["raw_html"] += "<div>Penalty imposed of ? 50,000 on Promoter. Note 1, 00, 000 shares seized. </div>"
            
        clean_obj = clean_and_tag(res)
        
        # Inject the deterministic PAN into the metadata to allow the RAG to pre-filter
        clean_obj["metadata"]["entity_pan"] = "ABCDE1234F"
        
        rag_objects.append(clean_obj)
        

    # -------------------------------------------------------------
    # STAGE 3: THE RAG PIPELINE (Storage & Retrieval)
    # -------------------------------------------------------------
    print("\n--- [STAGE 3] OCR CORRECTION & VECTORIZATION ---")
    all_chunks = []
    for ro in rag_objects:
        # A: OCR Correction Layer
        ro["content"] = correct_ocr_hallucinations(ro["content"])
        try:
            print(f"Cleaned Text: {ro['content'][-100:]}")
        except UnicodeEncodeError:
            safe_text = ro['content'][-100:].encode('ascii', errors='backslashreplace').decode('ascii')
            print(f"Cleaned Text (Safe): {safe_text}")
        
        # B: Spatial Chunker (Preserve tables vs standard text)
        doc_chunks = chunk_document(ro)
        all_chunks.extend(doc_chunks)
        
    # C: Embedding DB (FAISS storage)
    db.add_chunks(all_chunks)
    
    
    print("\n--- [STAGE 4] MULTI-HOP RETRIEVAL & VERIFICATION ---")
    
    # Run the modular retriever. It will strictly pre-filter for PAN=ABCDE1234F
    context_str = iterative_search(db, crawler_payload["entity_details"])
    
    print("Multi-Hop Retrieved Context:\n")
    try:
        print(context_str)
    except UnicodeEncodeError:
        print(context_str.encode('ascii', errors='backslashreplace').decode('ascii'))
    
    # THE HALLUCINATION GUARD TEST
    # We will simulate the Primary LLM generating two claims. 
    # One is supported by evidence. One is a complete hallucination.
    
    supported_claim = "The company has a pending lawsuit on e-Courts and faces a penalty of ₹ 50,000."
    hallucinated_claim = "The company's CEO Rahul Sharma was arrested by the CBI for a 100 crore money laundering scheme."
    
    print(f"\nEvaluating Supported Claim: '{supported_claim.encode('ascii', errors='backslashreplace').decode('ascii')}'")
    eval_1 = verify_findings(context_str, supported_claim)
    print(f"Verifier Output: {eval_1.encode('ascii', errors='backslashreplace').decode('ascii')}")
    
    print(f"\nEvaluating Hallucinated Claim: '{hallucinated_claim}'")
    eval_2 = verify_findings(context_str, hallucinated_claim)
    print(f"Verifier Output: {eval_2.encode('ascii', errors='backslashreplace').decode('ascii')}")
    
    
if __name__ == "__main__":
    asyncio.run(main())
