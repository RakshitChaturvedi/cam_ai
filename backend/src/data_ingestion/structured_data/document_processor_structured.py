from .structured_processor import process_structured_data

def process_structured_documents(file_paths):
    outputs = {}
    try:
        gst_file = file_paths.get("gst")
        bank_file = file_paths.get("bank")
        itr_file = file_paths.get("itr")

        results = process_structured_data(gst_file, bank_file, itr_file)
        outputs["structured_financial_analysis"] = results
    except Exception as e:
        print(f"Failed to process structured data: {e}")
    
    return outputs