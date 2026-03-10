import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# .env is at the project root (two levels above backend/src/)
load_dotenv(dotenv_path=Path(__file__).resolve().parents[4] / ".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(text, doc_type):

    if doc_type == "annual_report":

        return f"""
You are a corporate credit analyst.

Extract early warning signals from this annual report.

Return JSON with:

- entity_details
- promoter_details
- temporal_context
- contingent_liabilities
- capital_commitments
- corporate_guarantees
- related_party_transactions
- going_concern_issues
- debt_covenants
- impairments
- receivable_aging_risks

Mandatory: `entity_details` must be an object with keys: company_name, company_pan, cin, nic_code, pin_code. `promoter_details` must be a list of objects with keys: name, din, pan. `temporal_context` must be an object with keys: target_fy, start_date, end_date.

Text:
{text}
"""

    if doc_type == "legal_notice":

        return f"""
Extract legal financial risks.

Return JSON with:

- entity_details
- promoter_details
- temporal_context
- default_events
- insolvency_references
- section_138_cases
- arbitration_disputes
- liquidated_damages
- garnishee_orders

Mandatory: `entity_details` must be an object with keys: company_name, company_pan, cin, nic_code, pin_code. `promoter_details` must be a list of objects with keys: name, din, pan. `temporal_context` must be an object with keys: target_fy, start_date, end_date.

Text:
{text}
"""

    if doc_type == "sanction_letter":

        return f"""
Extract loan covenant risks.

Return JSON with:

- entity_details
- promoter_details
- temporal_context
- financial_covenants
- cross_default_clauses
- material_adverse_change
- right_to_setoff
- promoter_guarantee
- negative_lien

Mandatory: `entity_details` must be an object with keys: company_name, company_pan, cin, nic_code, pin_code. `promoter_details` must be a list of objects with keys: name, din, pan. `temporal_context` must be an object with keys: target_fy, start_date, end_date.

Text:
{text}
"""

    return f"Extract financial risks and a mandatory `entity_details`, `promoter_details`, and `temporal_context` object from text in JSON format: {text}"


def extract_signals_from_chunk(chunk, doc_type):

    prompt = build_prompt(chunk, doc_type)

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return completion.choices[0].message.content