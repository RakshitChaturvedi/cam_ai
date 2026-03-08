from data_ingestion.unstructured_data.document_processor import process_documents

def main():
    files = [
        "data/sample_annual_report.pdf",
        "data/sample_legal_notice.pdf",
        "data/sample_action_letter.pdf"
    ]

    results = process_documents(files)
    print("\n--- Extracted Signals ---\n")
    print(results)

if __name__ == "__main__":
    main()