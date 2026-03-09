from data_ingestion.unstructured_data.document_processor import process_documents
from data_ingestion.structured_data.document_processor_structured import process_structured_documents

import json

def main():
    unstructured_files = [
        "data/sample_annual_report.pdf",
        "data/sample_legal_notice.pdf",
        "data/sample_sanction_letter.pdf"
    ]
    unstructured_results = process_documents(unstructured_files)

    structured_files = {
        "gst":  "data/sample_gst.csv",
        "bank": "data/sample_bank.csv",
        "itr": "data/sample_itr.csv"
    }
    structured_results = process_structured_documents(structured_files)

    best_entity = {}
    
    for doc_type, docs in unstructured_results.items():
        for doc in docs:
            if "entity_resolution" in doc:
                entities = doc.pop("entity_resolution")
                for entity in entities:
                    meaningful_keys = [k for k in entity.keys() if k not in ("description", "source") and entity.get(k)]
                    best_meaningful = [k for k in best_entity.keys() if k not in ("description", "source") and best_entity.get(k)]
                    if len(meaningful_keys) > len(best_meaningful):
                        best_entity = entity.copy()

    best_entity.pop("description", None)
    best_entity.pop("source", None)

    crawler_payload = {
        "entity_resolution": best_entity
    }

    original_payload = {
        "unstructured_signals": unstructured_results,
        "structured_signals": structured_results
    }
    
    print("\n--- PAYLOAD 1: WEB CRAWLER TRIGGER ---\n")
    print(json.dumps(crawler_payload, indent=2))

    print("\n--- PAYLOAD 2: ORIGINAL DATA OUTPUT ---\n")
    print(json.dumps(original_payload, indent=2))

if __name__ == "__main__":
    main()