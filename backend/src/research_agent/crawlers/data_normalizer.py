from bs4 import BeautifulSoup
import datetime
import uuid
from typing import Dict, Any

def get_reliability_score(url: str) -> str:
    """
    Assigns a source reliability tag to enable downstream Conflict Resolution.
    """
    if ".gov.in" in url or ".nic.in" in url or ".org.in" in url:
        return "High/Official Government"
    if "livemint.com" in url or "economictimes" in url or "moneycontrol" in url:
        return "Medium/Reputable News"
    return "Low/Unverified Source"

def categorize_risk(engine_name: str) -> str:
    if engine_name == "litigation":
        return "Legal/Default Risk"
    if engine_name == "promoter":
        return "Governance/Shell Risk"
    if engine_name == "sector_risk":
        return "Sector Headwind"
    return "Unknown Risk"

def clean_and_tag(scrape_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Strips raw HTML boilerplate and returns clean JSON metadata for RAG ingestion.
    """
    raw_html = scrape_result.get("raw_html", "")
    source_url = scrape_result.get("source_url", "Unknown")
    engine = scrape_result.get("engine", "Unknown")
    
    # 1. Strip boiler HTML
    soup = BeautifulSoup(raw_html, "html.parser")
    clean_text = soup.get_text(separator=" ", strip=True)
    
    # 2. Tag Metadata
    return {
        "doc_id": f"scrape_{engine}_{uuid.uuid4().hex[:8]}",
        "content": clean_text,
        "metadata": {
            "source_url": source_url,
            "source_reliability": get_reliability_score(source_url),
            "date_published": datetime.datetime.now().strftime("%Y-%m-%d"),
            "risk_category": categorize_risk(engine)
        }
    }
