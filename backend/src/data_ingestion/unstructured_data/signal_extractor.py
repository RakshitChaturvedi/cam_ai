import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(text, doc_type):

    if doc_type == "annual_report":

        return f"""
You are a corporate credit analyst.

Extract early warning signals from this annual report.

Return JSON with:

- entity_resolution
- contingent_liabilities
- capital_commitments
- corporate_guarantees
- related_party_transactions
- going_concern_issues
- debt_covenants
- impairments
- receivable_aging_risks

Mandatory: `entity_resolution` must be a single JSON object containing company_name, registration_number, incorporation_date, and key_directors if found.

Text:
{text}
"""

    if doc_type == "legal_notice":

        return f"""
Extract legal financial risks.

Return JSON with:

- entity_resolution
- default_events
- insolvency_references
- section_138_cases
- arbitration_disputes
- liquidated_damages
- garnishee_orders

Mandatory: `entity_resolution` must be a single JSON object containing company_name, registration_number, incorporation_date, and key_directors if found.

Text:
{text}
"""

    if doc_type == "sanction_letter":

        return f"""
Extract loan covenant risks.

Return JSON with:

- entity_resolution
- financial_covenants
- cross_default_clauses
- material_adverse_change
- right_to_setoff
- promoter_guarantee
- negative_lien

Mandatory: `entity_resolution` must be a single JSON object containing company_name, registration_number, incorporation_date, and key_directors if found.

Text:
{text}
"""

    return f"Extract financial risks and a mandatory `entity_resolution` object (keys: company_name, registration_number, incorporation_date, key_directors) from text: {text}"


def extract_signals_from_chunk(chunk, doc_type):

    prompt = build_prompt(chunk, doc_type)

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return completion.choices[0].message.content