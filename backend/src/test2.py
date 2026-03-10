import requests
import json

url = "http://localhost:8000/api/analyze"
files = {
    "gst": ("sample_gst.csv", open("data/sample_gst.csv", "rb"), "text/csv"),
    "bank": ("sample_bank.csv", open("data/sample_bank.csv", "rb"), "text/csv"),
    "itr": ("sample_itr.csv", open("data/sample_itr.csv", "rb"), "text/csv"),
    "annual_report": ("sample_annual_report.pdf", open("data/sample_annual_report.pdf", "rb"), "application/pdf")
}

try:
    print("Testing external POST request...")
    res = requests.post(url, files=files)
    print("STATUS", res.status_code)
    try:
        print("RESP", json.dumps(res.json(), indent=2))
    except:
        print("TEXT", res.text)
except Exception as e:
    print("ERR", e)
