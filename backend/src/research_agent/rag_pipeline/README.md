# 📥 RAG Pipeline (Storage & Retrieval)

This module implements a state-of-the-art Retrieval-Augmented Generation (RAG) backend for free ($0 budget) using local embedding models and high-trust filtering.

## 📂 Components

- **`finmm_editor.py`**: A context-aware OCR correction layer. It uses Regex heuristics to fix common financial data halluciantions (e.g., converting `? 50,000` to `₹ 50,000` and `O` to `0`).
- **`spatial_chunker.py`**: A dual-path text splitter. It preserves tabular data using emulated spatial bounding boxes to ensure visual logic isn't destroyed by standard line splitting.
- **`embedding_db.py`**: Local vector storage using **FAISS** and `sentence-transformers` (`all-MiniLM-L6-v2`). Runs entirely offline with zero API costs.
- **`modular_retriever.py`**: Implements **Multi-Hop Search**. It pre-filters results strictly by entity PAN and iterates through multiple reasoning paths before sorting context by source reliability.
- **`refine_verifier.py`**: The **Hallucination Guard**. It cross-references generated LLM claims against the retrieved evidence and rejects any claims not explicitly found in the source documents.

## 🛡️ Trust Architecture
By combining **Spatial Preservation** with a **Deterministic Verifier**, this pipeline ensures that the final credit analysis is rooted 100% in evidence and is completely ungrounded from LLM fabrications.
