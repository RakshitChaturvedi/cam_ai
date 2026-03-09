def detect_revenue_mismatch(gst_records, bank_records):
    gst_sales = sum(record.get("amount", 0) for record in gst_records)
    bank_inflows = sum(record.get("amount", 0) for record in bank_records if str(record.get("type", "")).upper() == "CREDIT")

    if gst_sales == 0:
        ratio = 0
    else:
        ratio = bank_inflows / gst_sales

    return {
        "gst_sales": gst_sales,
        "bank_inflows": bank_inflows,
        "ratio": ratio,
        "revenue_inflation_flag": ratio < 0.7
    }
