
---

# CAM AI – Setup & Run Guide

This guide explains how to set up the project locally and run the **data ingestion pipelines**.

The system currently includes two pipelines:

* **Unstructured Data Ingestion** (PDF documents)
* **Structured Data Ingestion** (financial datasets)

---

# 1. Clone the Repository

Clone the project and move into the project directory.

```bash
git clone <repo_url>
cd cam_ai
```

---

# 2. Create Virtual Environment

Create and activate a Python virtual environment.

```bash
python -m venv venv
```

Activate it.

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

# 3. Install Dependencies

Install all required packages.

```bash
pip install -r requirements.txt
```

---

# 4. Environment Variables

Create a `.env` file in the **root folder** of the project.

```
cam_ai/
│
├── backend/
├── venv/
├── requirements.txt
└── .env
```

Add your Groq API key:

```text
GROQ_API_KEY=
```

Example:

```text
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxx
```

---

# 5. Add Data Files

Place the following files inside:

```text
backend/src/data/
```

Final structure:

```text
backend/src/data

sample_annual_report.pdf
sample_legal_notice.pdf
sample_sanction_letter.pdf

sample_gst.csv
sample_bank.csv
sample_itr.csv
```

These files are used for testing the **unstructured** and **structured** ingestion pipelines.

---

# 6. Project Structure

Important directories:

```text
backend/src

data_ingestion/

    unstructured_data/
        document_classifier.py
        document_profiles.py
        pdf_parser.py
        signal_extractor.py
        signal_aggregator.py
        signal_normalizer.py
        document_processor.py

    structured_data/
        gst_parser.py
        bank_parser.py
        itr_parser.py
        financial_normalizer.py
        circular_trading_detector.py
        revenue_mismatch_detector.py
        income_consistency_checker.py
        structured_data_processor.py

data/
    sample_annual_report.pdf
    sample_legal_notice.pdf
    sample_sanction_letter.pdf
    sample_gst.csv
    sample_bank.csv
    sample_itr.csv
```

---

# 7. Running the Full Application (Backend + Frontend)

The system now features a fully integrated React Frontend connecting to a FastAPI Python Backend running the ML Ensemble Pipeline.

You will need **TWO terminal windows** open to run this.

### Terminal 1: Start the Python Backend
Navigate to the `backend/src` folder and start the FastAPI server using Uvicorn:

```bash
cd backend/src

# Linux / macOS
export PYTHONPATH="."
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Windows (PowerShell)
$env:PYTHONPATH="."
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
*Wait until you see `Uvicorn running on http://0.0.0.0:8000` before starting the frontend.*

### Terminal 2: Start the React Frontend
Open a new terminal, navigate to the `frontend` folder, and start the Vite development server:

```bash
cd frontend
npm install   # If running for the first time
npm run dev
```

The application will now be live! Open your browser to `http://localhost:5173/` and click **"Start Processing"** to execute the real AI pipeline.

---

# 8. What the System Does

The system runs **two ingestion pipelines**.

---

## Unstructured Pipeline

Processes financial documents:

```text
Annual Reports
Legal Notices
Bank Sanction Letters
```

Steps:

```
PDF
↓
Text Extraction
↓
Document Classification
↓
Signal Extraction (LLM)
↓
Risk Signals
```

---

## Structured Pipeline

Processes financial datasets:

```text
GST filings
Bank statements
Income Tax Returns
```

Steps:

```
Financial datasets
↓
Parsing
↓
Normalization
↓
Financial anomaly detection
```

Detected anomalies include:

```
Circular trading
Revenue mismatch
Income inconsistency
```

---

# 9. Final Output

The system produces a combined ingestion result:

```json
{
  "unstructured_signals": {...},
  "structured_signals": {
    "structured_financial_analysis": {
      "financial_summary": {...},
      "circular_trading": {...},
      "revenue_mismatch": {...},
      "income_consistency": {...},
      "risk_summary": {...}
    }
  }
}
```

This output will later feed the **risk analysis and recommendation engine**.

---

# 10. Troubleshooting

### Missing API Key

Ensure `.env` contains:

```text
GROQ_API_KEY=
```

---

### Module Import Errors

Always run the program from:

```bash
backend/src
```

---

### Missing Data Files

Ensure all files are present in:

```text
backend/src/data/
```

---
