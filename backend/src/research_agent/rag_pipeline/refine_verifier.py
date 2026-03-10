import os
import json
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[4] / ".env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def verify_findings(context: str, generated_claim: str) -> str:
    """
    Missing Value Faithfulness Guardrail.
    Forces the LLM to prove its claim exists verbatim in the retrieved chunks.
    If it cannot find explicit schema linkage, it returns NULL.
    """
    
    prompt = f"""
You are a Strict Fact-Checking Verifier Agent.
Your job is to read an LLM's generated claim, and definitively verify if it is 100% supported by the retrieved context chunks.

[EXTRACTED CONTEXT CHUNKS]
{context}

[LLM GENERATED CLAIM TO VERIFY]
{generated_claim}

Rules:
1. If the claim introduces ANY names, numbers, or facts NOT explicitly present in the Context Chunks, it is a hallucination.
2. If the claim is hallucinated or lacks evidence, you MUST output perfectly: {{"verified": false, "corrected_output": "NULL: No Adverse Findings Supported by Evidence"}}
3. If the claim is fully supported, output: {{"verified": true, "corrected_output": "<Insert the original claim here>"}}

Output ONLY the JSON object.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        result = json.loads(completion.choices[0].message.content)
        return result.get("corrected_output", "NULL: Guardrail Parsing Error")
        
    except Exception as e:
        print(f"Verifier LLM Error: {e}")
        return "NULL: Guardrail API Error"
