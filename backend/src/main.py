from data_ingestion.unstructured_data.document_processor import process_documents

import json

def main():
    files = [
        "data/sample_annual_report.pdf",
        "data/sample_legal_notice.pdf",
        "data/sample_sanction_letter.pdf"
    ]

    results = process_documents(files)
    print("\n--- Extracted Signals ---\n")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()