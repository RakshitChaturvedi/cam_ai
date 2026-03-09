import pandas as pd

def parse_bank_statement(file_path):
    df = pd.read_csv(file_path)
    df.columns = [c.lower().strip() for c in df.columns]

    records = df.to_dict(orient="records")
    return records