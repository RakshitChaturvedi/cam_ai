from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
import shutil
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

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "CAM AI Backend is running."}

@app.post("/api/analyze")
async def execute_credit_analysis(
    annual_report: UploadFile = File(None),
    legal_notice: UploadFile = File(None),
    sanction_letter: UploadFile = File(None),
    gst: UploadFile = File(None),
    bank: UploadFile = File(None),
    itr: UploadFile = File(None)
):
    """
    Executes the entire backend pipeline and returns the consolidated JSON
    to the React frontend.
    """
    print("\n[API] Processing Analysis Request...")
    
    unstructured_files = []
    structured_files = {}

    def save_upload(upload_file: UploadFile):
        if not upload_file:
            return None
        filepath = os.path.join(UPLOAD_DIR, upload_file.filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return filepath

    # Handle unstructured
    ar_path = save_upload(annual_report)
    ln_path = save_upload(legal_notice)
    sl_path = save_upload(sanction_letter)
    
    if ar_path: unstructured_files.append(ar_path)
    if ln_path: unstructured_files.append(ln_path)
    if sl_path: unstructured_files.append(sl_path)
    
    if not unstructured_files:
        unstructured_files = None

    # Handle structured
    gst_path = save_upload(gst)
    bank_path = save_upload(bank)
    itr_path = save_upload(itr)
    
    if gst_path: structured_files["gst"] = gst_path
    if bank_path: structured_files["bank"] = bank_path
    if itr_path: structured_files["itr"] = itr_path
    
    if not structured_files:
        structured_files = None

    # 1. Run the Data Ingestion (Pillar 1)
    crawler_payload, original_payload = run_ingestion(unstructured_files, structured_files)
    
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
