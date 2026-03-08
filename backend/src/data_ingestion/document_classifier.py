def detect_document_type(pages):
    """
        Simple heuristic classifier based on first few pages.
    """

    text = " ".join([p["text"] for p in pages[:5]])

    if any(x in text for x in [
        "auditor",
        "financial statements",
        "balance sheet",
        "statement of profit",
        "notes to accounts"
    ]):
        return "annual_report"
    
    if "legal notice" in text or "section 138" in text or "insolvency" in text:
        return "legal_notice"
    
    if "sanction letter" in text or "loan facility" in text or "credit facility" in text:
        return "sanction_letter"

    return "unknown"