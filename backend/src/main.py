from data_ingestion.unstructured_data.document_processor import process_documents
from data_ingestion.structured_data.document_processor_structured import process_structured_documents

import json

def main():
    """
    unstructured_files = [
        "data/sample_annual_report.pdf",
        "data/sample_legal_notice.pdf",
        "data/sample_sanction_letter.pdf"
    ]
    unstructured_results = process_documents(unstructured_files)
    """
    structured_files = {
        "gst":  "data/sample_gst.csv",
        "bank": "data/sample_bank.csv",
        "itr": "data/sample_itr.csv"
    }
    structured_results = process_structured_documents(structured_files)

    final_result = {
        "unstructured_signals": 0, #unstructured_results,
        "structured_signals": structured_results
    }
    print("\n--- FINAL INGESTION OUTPUT ---\n")
    print(json.dumps(final_result, indent=2))

if __name__ == "__main__":
    main()