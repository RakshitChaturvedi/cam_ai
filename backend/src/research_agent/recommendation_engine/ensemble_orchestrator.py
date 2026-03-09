import os
import json
import asyncio
from typing import Dict, Any, List
from groq import Groq
from dotenv import load_dotenv

from research_agent.recommendation_engine.prompt_permutations import get_prompts

load_dotenv()

# We will simulate the Ensemble purely through Groq's multi-model catalog to ensure $0 cost and speed,
# but architecturally this represents Llama vs Gemini vs DeepSeek.
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# If you configure Gemini or OpenRouter, add the logic below, otherwise fallback to Groq models
# to guarantee the script runs right out of the box.
MODELS = [
    "llama-3.3-70b-versatile", # Simulating Model 1 (e.g., The Heavy Reasoner)
    "llama-3.1-8b-instant",    # Simulating Model 2 (e.g., The Fast Classifier)
    "gemma2-9b-it"             # Simulating Model 3 (e.g., The MoE Arbitrator)
]

async def _fetch_llm_decision(prompt_name: str, system_prompt: str, model_name: str, context_str: str) -> dict:
    """Async call to the LLM to get one of the 9 JSON responses."""
    
    full_prompt = f"""
{system_prompt}

### Context:
{context_str}
    """
    
    try:
        # Wrap the synchronous Groq client inside an asyncio thread for speed
        loop = asyncio.get_event_loop()
        completion = await loop.run_in_executor(
            None, 
            lambda: groq_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": full_prompt}],
                response_format={"type": "json_object"}
            )
        )
        
        result = json.loads(completion.choices[0].message.content)
        result["metadata"] = {"prompt": prompt_name, "model": model_name}
        return result
        
    except Exception as e:
        print(f"Error fetching from {model_name} with {prompt_name}: {e}")
        return {
            "approval_status": "Reject",
            "recommended_limit_inr": 0,
            "risk_premium_percentage": 0.0,
            "core_rationale": "API Timeout or Parsing Error. Defaulting to Reject.",
            "metadata": {"prompt": prompt_name, "model": model_name, "error": str(e)}
        }


async def run_ensemble(
    structured_json: Dict, 
    unstructured_json: Dict, 
    rag_context: str, 
    hitl_json: Dict
) -> List[Dict]:
    """
    The ML-Based Evaluator.
    Fires the 3 prompts across the 3 LLMs (9 total calls).
    """
    
    # 1. Compile the payload string
    context_str = f"""
* Financial Summary: {json.dumps(structured_json)}
* Extracted Document Risks: {json.dumps(unstructured_json)}
* Secondary Web Intelligence [RAG EVIDENCE]: {rag_context}
* Credit Officer Adjustments: {json.dumps(hitl_json)}
    """
    
    prompts = get_prompts()
    
    tasks = []
    
    # Generate the permutation grid
    for prompt_name, prompt_text in prompts.items():
        for model in MODELS:
            tasks.append(_fetch_llm_decision(prompt_name, prompt_text, model, context_str))
            
    print(f"Orchestrator firing {len(tasks)} concurrent LLM evaluations...")
    results = await asyncio.gather(*tasks)
    
    return list(results)
