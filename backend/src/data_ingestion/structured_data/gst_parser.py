import pandas as pd

def parse_gst_file(file_path):
    df = pd.read_csv(file_path)
    df.columns = [c.lower().strip() for c in df.columns]

    required = ["seller_gstin", "buyer_gstin", "amount"]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
    
    records = df.to_dict(orient="records")
    return records