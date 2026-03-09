# 🕸️ Automated Crawlers (Hybrid Neuro-Symbolic)

This module handles the real-time extraction of data from official Indian regulatory portals and financial news sources. It solves the "Static Data" problem by fetching live litigation and promoter status.

## 📂 Components

- **`payload_receiver.py`**: The gatekeeper. It validates incoming entity data from the Ingestion Layer using Regex patterns (PAN, DIN) and flags missing identifiers for LLM-based query construction.
- **`query_architect.py`**: A hybrid engine. If identifiers are present, it uses deterministic Boolean logic for search queries. If identifiers are missing, it uses Llama-3 to generate robust, context-aware queries.
- **`engines/`**: Multi-threaded scraper stubs targeting:
  - `litigation.py`: e-Courts and CIBIL databases.
  - `promoter.py`: MCA portal for directorships and shell risks.
  - `sector_risk.py`: RBI/SEBI announcements and financial news.
- **`data_normalizer.py`**: Cleans raw HTML using BeautifulSoup and attaches metadata tags (`source_reliability`, `date_published`) for downstream ingestion into RAG.

## 🚀 Key Innovation
The module uses **Neuro-Symbolic** search—pairing strict regulatory identifiers with LLM fallback—to guarantee that search results are mathematically precise yet resilient to OCR noise.
