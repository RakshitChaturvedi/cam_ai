from typing import List, Dict
import statistics

def calculate_ml_confidence(ensemble_responses: List[Dict]) -> Dict:
    """
    Translates the 9 ungrounded LLM responses into a strictly Deterministic,
    explainable Confidence Score and Credit Recommendation.
    """
    
    total_votes = len(ensemble_responses)
    if total_votes == 0:
        return {"error": "No LLM responses to vote on."}
        
    approval_count = 0
    rejection_count = 0
    
    limits = []
    premiums = []
    rationales = []
    
    for r in ensemble_responses:
        status = r.get("approval_status", "Reject").strip().title()
        if status == "Approve":
            approval_count += 1
            # Only append the terms if they approved it (don't average rejected numbers)
            limit = r.get("recommended_limit_inr", 0)
            if limit > 0: limits.append(limit)
                
            premium = r.get("risk_premium_percentage", 0.0)
            if premium > 0: premiums.append(premium)
                
        else:
            rejection_count += 1
            
        # Collect the rationale, preferably from the heaviest model
        meta = r.get("metadata", {})
        if "70b" in meta.get("model", ""):
            rationales.append(r.get("core_rationale", ""))
            
            
    # Calculate Final Decision via Majority Rules
    final_decision = "Approve" if approval_count > rejection_count else "Reject"
    
    # Calculate Confidence Score (%)
    winning_votes = approval_count if final_decision == "Approve" else rejection_count
    confidence_percentage = round((winning_votes / total_votes) * 100, 2)
    
    # Calculate Weighted Averages (Medians preferred to prevent single-prompt extreme outliers)
    final_limit = int(statistics.median(limits)) if limits and final_decision == "Approve" else 0
    final_premium = round(statistics.median(premiums), 2) if premiums and final_decision == "Approve" else 0.0
    
    # Select the best Rationale explicitly for Explainability
    # Grab the first available 'Heavy' model rationale, or fallback
    final_rationale = rationales[0] if rationales else ensemble_responses[0].get("core_rationale", "Unknown rationale.")
    
    return {
        "final_decision": final_decision,
        "ml_confidence_score": f"{confidence_percentage}%",
        "winning_votes": f"{winning_votes}/{total_votes}",
        "recommended_limit_inr": final_limit,
        "risk_premium_percentage": final_premium,
        "primary_explainable_rationale": final_rationale
    }
