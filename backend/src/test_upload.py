import requests

url = "http://localhost:8000/api/analyze"
files = {
    "gst": ("sample_gst.csv", open("data/sample_gst.csv", "rb"), "text/csv"),
    "bank": ("sample_bank.csv", open("data/sample_bank.csv", "rb"), "text/csv"),
}
res = requests.post(url, files=files)
print(res.status_code)
print(res.json())
