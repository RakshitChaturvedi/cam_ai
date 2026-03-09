import json
import os
from groq import Groq
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Phase A: Deterministic Rule-Based Mapping
NIC_MAP = {
    "13": "Textiles Ministry", 
    "64": "Reserve Bank of India (RBI)"
}

PIN_MAP = {
    "400001": "Mumbai District Court"
}


def build_fallback_prompt(payload: Dict[str, Any]) -> str:
    """
    Constructs the exact fallback prompt.
    """
    entity = payload.get("entity_details", {})
    promoters = payload.get("promoter_details", [])
    temp = payload.get("temporal_context", {})

    company_name = entity.get("company_name", "Unknown")
    company_pan = entity.get("company_pan", "Unknown")
    cin = entity.get("cin", "Unknown")

    start_date = temp.get("start_date", "Unknown")
    end_date = temp.get("end_date", "Unknown")
    
    # Just grab all anomalies found during ingestion for context
    flags = "Potential Revenue Mismatch, Potential Default History" 

    return f"""
You are a deterministic query-construction agent for an Indian Corporate Credit Decisioning Engine. 
Your task is to construct highly targeted, boolean web-search queries to find secondary intelligence on a borrower.

###Context:
*   Company Name: {company_name}
*   Known Identifiers: {company_pan}, {cin}
*   Target Financial Year: {start_date} to {end_date}
*   Identified Anomaly/Issue: {flags}

###Instructions:
1. Alias Generation: Create semantic variations of the company name (e.g., "Pvt Ltd" to "Private Limited").
2. Temporal Bounding: Strictly bound all queries between the start_date and end_date to ignore outdated distractor news.
3. Domain Targeting: Target specific Indian regulatory and legal domains based on the context. 
4. Missing Value Faithfulness: Do NOT invent identifiers. If a PAN or CIN is missing, rely strictly on Name + Location.

Output a JSON object with the exact queries to be passed to the scraping engines:
{{
  "litigation_query": "(<aliases>) AND ('lawsuit' OR 'defaulter' OR 'NCLT') site:ecourts.gov.in",
  "regulatory_query": "(<industry_type>) AND ('regulation' OR 'headwind' OR 'penalty') site:rbi.org.in OR site:sebi.gov.in",
  "promoter_query": "(<promoter_name>) AND ('fraud' OR 'shell company' OR 'ED investigation')"
}}
    """

def construct_queries(payload_metadata: Dict[str, Any]) -> Dict[str, str]:
    """
    Phase B: The Hybrid Constructor Engine 
    """
    needs_fallback = payload_metadata.get("needs_llm_fallback", False)
    payload = payload_metadata.get("payload", {})
    
    # Base Initialization
    queries = {
        "litigation_query": "",
        "regulatory_query": "",
        "promoter_query": ""
    }
    
    if needs_fallback:
        print("Deterministic identifiers lacking. Falling back to LLM Query Construction...")
        prompt = build_fallback_prompt(payload)
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            llm_queries = json.loads(completion.choices[0].message.content)
            queries.update(llm_queries)
        except Exception as e:
            print(f"LLM Query Generation failed: {e}")
    else:
        print("Deterministic identifiers present. Using Rule-Based Constructor...")
        
        entity = payload.get("entity_details", {})
        promoters = payload.get("promoter_details", [])
        
        c_name = entity.get("company_name", "")
        pan = entity.get("company_pan", "")
        nic = str(entity.get("nic_code", ""))
        
        # Pull deterministic map logic
        industry = NIC_MAP.get(nic, "General Industry")
        
        # Construct deterministic litigation target
        queries["litigation_query"] = f'("{c_name}" OR "{pan}") AND ("lawsuit" OR "defaulter" OR "NCLT") site:ecourts.gov.in'
        
        # Construct deterministic regulatory target
        queries["regulatory_query"] = f'("{industry}") AND ("regulation" OR "headwind" OR "penalty") site:rbi.org.in OR site:sebi.gov.in'
        
        # Construct deterministic promoter target
        if promoters:
            p_name = promoters[0].get("name", "")
            queries["promoter_query"] = f'("{p_name}") AND ("fraud" OR "shell company" OR "ED investigation")'
            
    return queries
