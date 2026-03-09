import pandas as pd

def parse_itr_file(file_path):
    df = pd.read_csv(file_path)
    df.columns = [c.lower().strip() for c in df.columns]

    records = df.to_dict(orient="records")
    return records
    