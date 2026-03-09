from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from pydantic import BaseModel

# Import our backend logical pipelines
from main import run_ingestion
from research_agent.recommendation_engine.ensemble_orchestrator import run_ensemble
from research_agent.recommendation_engine.majority_voter import calculate_ml_confidence

app = FastAPI(title="CAM AI - Credit Appraisal Engine")

# Enable CORS for the React Frontend (Vite default port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "CAM AI Backend is running."}

@app.get("/api/analyze")
async def execute_credit_analysis():
    """
    Executes the entire backend pipeline and returns the consolidated JSON
    to the React frontend.
    """
    print("\n[API] Processing Analysis Request...")
    
    # 1. Run the Data Ingestion (Pillar 1)
    crawler_payload, original_payload = run_ingestion()
    
    # Extract the structured and unstructured pieces for the orchestrator
    structured_json = original_payload.get("structured_signals", {})
    unstructured_json = original_payload.get("unstructured_signals", {})
    
    # 2. Run the RAG Pipeline Retrieval (Pillar 2 Mock for Demo speed)
    # The actual RAG spins up FAISS which takes ~10 seconds. We'll use the validated output.
    mock_rag_context = "The company has a clean regulatory record with the RBI. No recent penalties found. Industry headwinds are moderate but stable."
    
    # 3. Simulate Human-In-The-Loop Field Notes (Pillar 3)
    mock_hitl = {
        "adjusted_scores": {"Character": 80, "Capacity": 92, "Capital": 90, "Collateral": 70, "Conditions": 80},
        "adjustment_log": ["Baseline Capacity Score was 80/100. Added 12 points due to Positive Field Note: Factory is running 3 shifts at maximum efficiency."]
    }
    
    # 4. Run the ML Recommendation Engine (Pillar 4)
    print("[API] Firing ML Ensemble Orchestrator...")
    ensemble_responses = await run_ensemble(
        structured_json,
        unstructured_json,
        mock_rag_context,
        mock_hitl
    )
    
    final_decision = calculate_ml_confidence(ensemble_responses)
    print("[API] Ensemble Decision Calculated:", final_decision)
    
    # 5. Compile the Final Payload for React
    # Note: original_payload already contains `unstructured_signals` and `structured_signals` 
    # required by the Dashboard.jsx components!
    final_payload = original_payload.copy()
    final_payload["recommendation_payload"] = final_decision
    
    return final_payload
