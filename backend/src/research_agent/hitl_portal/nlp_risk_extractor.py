import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_risk_metadata(officer_input_text: str) -> dict:
    """
    Categorizes a qualitative field note into the Five Cs of Credit.
    Returns Sentiment and Severity Score.
    """
    
    prompt = f"""
You are a qualitative risk analyzer for an Indian Corporate Credit Engine. 
Read the Credit Officer's field note and extract the risk implications.

### Field Note: "{officer_input_text}"

### Instructions:
1. Map the note to ONE of the Five Cs of Credit: Character, Capacity, Capital, Collateral, or Conditions.
2. Determine the Sentiment: Positive, Neutral, or Negative.
3. Assign a Severity Score from 1 (Low Impact) to 5 (Critical Impact).
4. Provide a 1-sentence Summary Reason.

Output STRICTLY in JSON format:
{{
  "mapped_category": "Capacity",
  "sentiment": "Negative",
  "severity_score": 4,
  "summary_reason": "Factory underutilization indicates potential cash flow and revenue generation issues."
}}
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        result = json.loads(completion.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"NLP Extractor LLM Error: {e}")
        return {
            "mapped_category": "Unknown",
            "sentiment": "Neutral",
            "severity_score": 0,
            "summary_reason": "Failed to parse input."
        }
