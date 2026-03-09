from .pdf_parser import parse_pdf

def process_documents(file_paths):
    """
        Process multiple documents
        Return signals grouped by docs.
    """

    outputs = {}

    for path in file_paths:
        try:
            result = parse_pdf(path)
            doc_type = result["document_type"]
            signals = result["signals"]

            if doc_type not in outputs:
                outputs[doc_type] = []
            outputs[doc_type] = signals
        except Exception as e:
            print(f"Failed to process {path}: {e}")
        
    return outputs