import asyncio
import json

from ensemble_orchestrator import run_ensemble
from majority_voter import calculate_ml_confidence
from cam_generator import generate_cam_report

async def test_recommendation_pipeline():
    print("=========================================================")
    print("      ML RECOMMENDATION TEST: ORCHESTRATOR -> CAM FORMATTER")
    print("=========================================================")
    
    # MOCK INPUT 1: Structured Data (From Pillar 1)
    mock_structured = {
        "revenue_matches": True,
        "gst_turnover": 50000000,
        "bank_inflow": 49000000
    }
    
    # MOCK INPUT 2: Unstructured Data (From Pillar 1)
    mock_unstructured = {
        "lawsuit_detected": False,
        "nclt_flag": False
    }
    
    # MOCK INPUT 3: RAG Retrieval (From Pillar 2)
    mock_rag = "The company has a clean regulatory record with the RBI. No recent penalties found. Industry headwinds are moderate but stable."
    
    # MOCK INPUT 4: HITL Portal Log (From Pillar 3)
    mock_hitl = {
        "adjusted_scores": {
            "Character": 80,
            "Capacity": 92,
            "Capital": 90,
            "Collateral": 70,
            "Conditions": 80
        },
        "adjustment_log": [
             "Baseline Capacity Score was 80/100. Added 12 points due to Positive Field Note: Factory is running 3 shifts at maximum efficiency."
        ]
    }
    
    print("\n>>> FIRING CONCURRENT ENSEMBLE ORCHESTRATOR (3 Prompts x 3 Models)...")
    # This will generate 9 total output decisions
    ensemble_responses = await run_ensemble(
        mock_structured,
        mock_unstructured,
        mock_rag,
        mock_hitl
    )
    
    print(f"\n[ENSEMBLE COMPLETE] Received {len(ensemble_responses)} unstructured LLM Opinions.")
    for idx, resp in enumerate(ensemble_responses):
        print(f"Model ID {idx}: Prompt={resp.get('metadata', {}).get('prompt')} -> Status: {resp.get('approval_status')}")
    
    print("\n>>> APPLYING DETERMINISTIC MAJORITY VOTE...")
    final_decision = calculate_ml_confidence(ensemble_responses)
    
    print(json.dumps(final_decision, indent=2))
    
    print("\n>>> GENERATING FINAL DOCX CREDIT APPRAISAL MEMO (CAM)...")
    generate_cam_report(
        entity_name="ABC Manufacturing Pvt. Ltd.",
        majority_decision=final_decision,
        hitl_input=mock_hitl,
        output_filename="TEST_OUTPUT_CAM.docx"
    )
    
if __name__ == "__main__":
    asyncio.run(test_recommendation_pipeline())
