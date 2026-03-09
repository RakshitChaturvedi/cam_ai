def adjust_credit_score(nlp_payload: dict, current_baseline_scores: dict) -> dict:
    """
    Deterministic rule-based adjuster.
    Takes the NLP Extracted JSON and applies math to prevent LLM hallucination.
    """
    
    category = nlp_payload.get("mapped_category", "Unknown")
    sentiment = nlp_payload.get("sentiment", "Neutral")
    severity = nlp_payload.get("severity_score", 0)
    reason = nlp_payload.get("summary_reason", "No reason provided.")
    
    # Initialize the output payload
    result = {
        "adjusted_scores": current_baseline_scores.copy(),
        "adjustment_log": []
    }
    
    if category not in current_baseline_scores:
        result["adjustment_log"].append(f"Skipped adjustment: '{category}' is not a tracked C of Credit.")
        return result
        
    old_score = current_baseline_scores[category]
    adjustment_value = severity * 2
    
    if sentiment.lower() == "negative":
        new_score = old_score - adjustment_value
        log_entry = f"Baseline {category} Score was {old_score}/100. Deducted {adjustment_value} points due to Negative Field Note: {reason}"
        
    elif sentiment.lower() == "positive":
        new_score = old_score + adjustment_value
        # Cap at 100
        new_score = min(100, new_score)
        log_entry = f"Baseline {category} Score was {old_score}/100. Added {adjustment_value} points due to Positive Field Note: {reason}"
        
    else: # Neutral
        new_score = old_score
        log_entry = f"Baseline {category} Score was {old_score}/100. No adjustment made (Neutral Field Note)."
        
    # Prevent negative scores
    new_score = max(0, new_score)
    
    # Update the tracking dicts
    result["adjusted_scores"][category] = new_score
    result["adjustment_log"].append(log_entry)
    
    return result
