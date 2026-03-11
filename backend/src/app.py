from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
import json
import shutil
from pydantic import BaseModel
from typing import Optional, Dict, List

# Import our backend logical pipelines
from main import run_ingestion
from research_agent.recommendation_engine.ensemble_orchestrator import run_ensemble
from research_agent.recommendation_engine.majority_voter import calculate_ml_confidence
from research_agent.hitl_portal.nlp_risk_extractor import extract_risk_metadata
from research_agent.hitl_portal.dynamic_scorer import adjust_credit_score


class HITLNoteRequest(BaseModel):
    note: str
    source: str = "General Observation"
    baseline_scores: Dict[str, int] = {
        "Character": 80, "Capacity": 80, "Capital": 80, "Collateral": 80, "Conditions": 80
    }

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

def save_upload(upload_file: UploadFile):
    """Save an uploaded file to disk and return its path."""
    if not upload_file:
        return None
    filepath = os.path.join(UPLOAD_DIR, upload_file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return filepath

@app.get("/")
def read_root():
    return {"status": "ok", "message": "CAM AI Backend is running."}

@app.post("/api/entity-extract")
async def extract_entity_details(
    annual_report: UploadFile = File(None),
    legal_notice: UploadFile = File(None),
    sanction_letter: UploadFile = File(None),
    gst: UploadFile = File(None),
    bank: UploadFile = File(None),
    itr: UploadFile = File(None)
):
    """
    Lightweight endpoint: runs only Data Ingestion to extract entity details
    (Company PAN, CIN, Promoter DINs) without triggering the full ML pipeline.
    """
    print("\n[API] Entity Extraction Request...")

    unstructured_files = []
    structured_files = {}

    ar_path = save_upload(annual_report)
    ln_path = save_upload(legal_notice)
    sl_path = save_upload(sanction_letter)

    if ar_path: unstructured_files.append(ar_path)
    if ln_path: unstructured_files.append(ln_path)
    if sl_path: unstructured_files.append(sl_path)

    if not unstructured_files:
        unstructured_files = None

    gst_path = save_upload(gst)
    bank_path = save_upload(bank)
    itr_path = save_upload(itr)

    if gst_path: structured_files["gst"] = gst_path
    if bank_path: structured_files["bank"] = bank_path
    if itr_path: structured_files["itr"] = itr_path

    if not structured_files:
        structured_files = None

    crawler_payload, _ = run_ingestion(unstructured_files, structured_files)

    return crawler_payload


@app.post("/api/hitl-process")
async def process_hitl_note(request: HITLNoteRequest):
    """
    Processes a single credit officer field note through the NLP extractor
    and deterministic scorer. Returns the NLP metadata + adjusted scores.
    """
    print(f"\n[API] HITL Note Received: '{request.note}' (Source: {request.source})")

    # 1. NLP Extraction via Llama-3
    nlp_data = extract_risk_metadata(request.note)
    nlp_data["source_document"] = request.source

    # 2. Deterministic Score Adjustment
    adjustment_result = adjust_credit_score(nlp_data, request.baseline_scores)

    return {
        "nlp_extraction": nlp_data,
        "adjusted_scores": adjustment_result["adjusted_scores"],
        "adjustment_log": adjustment_result["adjustment_log"]
    }

@app.post("/api/analyze")
async def execute_credit_analysis(
    annual_report: UploadFile = File(None),
    legal_notice: UploadFile = File(None),
    sanction_letter: UploadFile = File(None),
    gst: UploadFile = File(None),
    bank: UploadFile = File(None),
    itr: UploadFile = File(None),
    hitl_data: Optional[str] = Form(None)
):
    """
    Executes the entire backend pipeline and returns the consolidated JSON
    to the React frontend.
    """
    print("\n[API] Processing Analysis Request...")
    
    unstructured_files = []
    structured_files = {}

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
    
    # 3. Human-In-The-Loop Field Notes (Pillar 3)
    if hitl_data:
        try:
            hitl_json = json.loads(hitl_data)
        except json.JSONDecodeError:
            hitl_json = {
                "adjusted_scores": {"Character": 80, "Capacity": 80, "Capital": 80, "Collateral": 80, "Conditions": 80},
                "adjustment_log": []
            }
    else:
        # Fallback to defaults if no HITL data provided
        hitl_json = {
            "adjusted_scores": {"Character": 80, "Capacity": 80, "Capital": 80, "Collateral": 80, "Conditions": 80},
            "adjustment_log": []
        }
    
    # 4. Run the ML Recommendation Engine (Pillar 4)
    print("[API] Firing ML Ensemble Orchestrator...")
    ensemble_responses = await run_ensemble(
        structured_json,
        unstructured_json,
        mock_rag_context,
        hitl_json
    )
    
    final_decision = calculate_ml_confidence(ensemble_responses)
    print("[API] Ensemble Decision Calculated:", final_decision)
    
    # 5. Compile the Final Payload for React
    # Note: original_payload already contains `unstructured_signals` and `structured_signals` 
    # required by the Dashboard.jsx components!
    final_payload = original_payload.copy()
    final_payload["recommendation_payload"] = final_decision
    
    return final_payload
