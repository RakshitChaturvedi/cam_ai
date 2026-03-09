def normalize_financial_data(gst_records, bank_records, itr_records):
    gst_sales = sum(r.get("amount", 0) for r in gst_records)
    bank_inflows = sum(r.get("amount",0) for r in bank_records if str(r.get("type", "")).upper() == "CREDIT")
    itr_income = 0
    if itr_records:
        itr_income = itr_records[0].get("total_income", 0)

    return {
        "gst_sales": gst_sales,
        "bank_inflows": bank_inflows,
        "itr_income": itr_income
    }
