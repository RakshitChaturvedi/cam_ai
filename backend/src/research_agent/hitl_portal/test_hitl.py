from nlp_risk_extractor import extract_risk_metadata
from dynamic_scorer import adjust_credit_score
import json

def test_hitl_pipeline():
    print("=========================================================")
    print("      HITL PORTAL BACKEND TEST: NLP -> DETERMINISTIC     ")
    print("=========================================================")
    
    # Mocking the existing Credit Profile state
    baseline_scores = {
        "Character": 80,
        "Capacity": 85,
        "Capital": 90,
        "Collateral": 70,
        "Conditions": 80
    }
    
    print("\n[MOCK BASELINE SCORES]")
    print(json.dumps(baseline_scores, indent=2))
    
    test_notes = [
        "Factory visited on Tuesday. Operating at roughly 40% capacity, several assembly lines shut down.",
        "Met with the new CFO. They just secured a massive 50 crore capital injection from a Tier 1 VC."
    ]
    
    for idx, note in enumerate(test_notes):
        print(f"\n\n--- PROCESSING NOTE #{idx + 1} ---")
        print(f"Credit Officer Input: '{note}'")
        
        # 1. LLM NLP Extraction
        print("\n>>> Extracting Metadata via Llama-3...")
        nlp_data = extract_risk_metadata(note)
        print(json.dumps(nlp_data, indent=2))
        
        # 2. Deterministic Math Adjuster
        print("\n>>> Applying Deterministic Math Rules...")
        adjustment_result = adjust_credit_score(nlp_data, baseline_scores)
        
        print("\n[EXPLAINABLE ADJUSTMENT LOG]")
        for log in adjustment_result['adjustment_log']:
            print(f"- {log}")
            
        print("\n[NEW ADJUSTED SCORES]")
        # Update the baseline for the next simulated loop
        baseline_scores = adjustment_result["adjusted_scores"]
        print(json.dumps(baseline_scores, indent=2))
        
if __name__ == "__main__":
    test_hitl_pipeline()
