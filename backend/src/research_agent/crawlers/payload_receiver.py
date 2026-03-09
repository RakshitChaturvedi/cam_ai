import re
from typing import Dict, Any, Tuple

def validate_payload(payload: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """
    Validates incoming data from the Data Ingestion layer.
    Runs deterministic regex checks to prevent junk searches.
    Returns (is_valid, payload)
    """
    
    if not payload.get("entity_details"):
        return False, {"error": "Missing entity_details block"}
        
    entity_details = payload["entity_details"]
    
    # 1. Validate PAN (Pattern: 5 Letters, 4 Numbers, 1 Letter)
    company_pan = entity_details.get("company_pan")
    if company_pan and not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", str(company_pan)):
        company_pan = None # Malformed
        
    # 2. Validate DINs if promoters exist
    promoters = payload.get("promoter_details", [])
    valid_promoters = []
    
    for promoter in promoters:
        din = promoter.get("din")
        # DIN is an 8-digit string
        if din and re.match(r"^[0-9]{8}$", str(din)):
            valid_promoters.append(promoter)
            
    # If deterministic identifiers (PAN or valid DINs) are missing/malformed, 
    # we flag this for LLM Fallback (handled downstream by the query architect)
    needs_fallback = not company_pan or not valid_promoters
    
    return True, {
        "needs_llm_fallback": needs_fallback,
        "payload": payload
    }
