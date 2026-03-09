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

    best_entity_details = {}
    best_promoter_details = []
    best_temporal_context = {}
    
    for doc_type, docs in unstructured_results.items():
        for doc in docs:
            # Extract and evaluate entity_details
            if "entity_details" in doc:
                entities = doc.pop("entity_details")
                for entity in entities:
                    if not isinstance(entity, dict): continue
                    meaningful_keys = [k for k in entity.keys() if k not in ("description", "source") and entity.get(k)]
                    best_meaningful = [k for k in best_entity_details.keys() if k not in ("description", "source") and best_entity_details.get(k)]
                    if len(meaningful_keys) > len(best_meaningful):
                        best_entity_details = entity.copy()
            # Extract and evaluate promoter_details
            if "promoter_details" in doc:
                promoters = doc.pop("promoter_details")
                for p in promoters: # Often wrapped in arrays
                    if isinstance(p, dict) and p.get("name"):
                        # Just aggregate all unique promoters found
                        p.pop("description", None)
                        p.pop("source", None)
                        if p not in best_promoter_details:
                            best_promoter_details.append(p)
                    elif isinstance(p, list):
                         for sub_p in p:
                              if isinstance(sub_p, dict) and sub_p.get("name"):
                                  sub_p.pop("description", None)
                                  sub_p.pop("source", None)
                                  if sub_p not in best_promoter_details:
                                      best_promoter_details.append(sub_p)

            # Extract temporal_context
            if "temporal_context" in doc:
                contexts = doc.pop("temporal_context")
                for ctx in contexts:
                    if not isinstance(ctx, dict): continue
                    meaningful_keys = [k for k in ctx.keys() if k not in ("description", "source") and ctx.get(k)]
                    best_meaningful = [k for k in best_temporal_context.keys() if k not in ("description", "source") and best_temporal_context.get(k)]
                    if len(meaningful_keys) > len(best_meaningful):
                        best_temporal_context = ctx.copy()

    best_entity_details.pop("description", None)
    best_entity_details.pop("source", None)
    best_temporal_context.pop("description", None)
    best_temporal_context.pop("source", None)

    crawler_payload = {
        "entity_details": best_entity_details,
        "promoter_details": best_promoter_details,
        "temporal_context": best_temporal_context
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