import json
import asyncio
from crawlers.payload_receiver import validate_payload
from crawlers.query_architect import construct_queries
from crawlers.engines import litigation, promoter, sector_risk
from crawlers.data_normalizer import clean_and_tag

async def main():
    # Simulated crawler_payload from Data Ingestion (Payload 1)
    crawler_payload = {
        "entity_details": {
            # Intentionally breaking PAN format to trigger LLM fallback behavior for testing
            "company_name": "ABC Textiles Pvt Ltd",
            "company_pan": "INVALID_PAN123",  # Malformed to trigger LLM fallback
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
    
    print("\n--- [1] PAYLOAD RECEIVED FROM INGESTION ---")
    print(json.dumps(crawler_payload, indent=2))
    
    # 1. Validation & Fallback Check
    is_valid, validation_data = validate_payload(crawler_payload)
    if not is_valid:
        print(f"Payload validation failed: {validation_data.get('error')}")
        return
        
    print(f"\n--- [2] VALIDATION COMPLETE ---")
    print(f"Needs LLM Fallback (Due to missing/bad identifiers)? {validation_data['needs_llm_fallback']}")
    
    # 2. Query Architecture
    print("\n--- [3] CONSTRUCTING CRAWLER QUERIES ---")
    queries_dict = construct_queries(validation_data)
    print(json.dumps(queries_dict, indent=2))
    
    # 3. Parallel Execution of Scraping Engines
    print("\n--- [4] EXECUTING SCRAPER ENGINES ---")
    
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
    
    # Run async scraping in parallel
    results = await asyncio.gather(lit_task, prom_task, sec_task)
    
    # 4. Normalization and Metadata Tagging for RAG Output
    print("\n--- [5] CLEANING & NORMALIZING FOR RAG DB ---")
    final_rag_db_objects = []
    
    for scrape_res in results:
        rag_object = clean_and_tag(scrape_res)
        final_rag_db_objects.append(rag_object)
        
    print(json.dumps(final_rag_db_objects, indent=2))
    
if __name__ == "__main__":
    asyncio.run(main())
