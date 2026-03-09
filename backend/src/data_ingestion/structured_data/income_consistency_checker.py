def check_income_consistency(gst_records, itr_records):
    gst_sales = sum(record.get("amount", 0) for record in gst_records)
    itr_income = 0

    if itr_records:
        itr_income = itr_records[0].get("total_income", 0)
    
    if gst_sales == 0:
        ratio = 0
    else:
        ratio = itr_income / gst_sales

    return {
        "gst_sales": gst_sales,
        "itr_income": itr_income,
        "income_ratio": ratio,
        "income_inconsistency_flag": ratio < 0.1
    }