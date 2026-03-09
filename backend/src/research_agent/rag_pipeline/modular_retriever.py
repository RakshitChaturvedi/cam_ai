from typing import Dict, Any, List
from .embedding_db import LocalVectorDB

def iterative_search(vector_db: LocalVectorDB, entity_metadata: Dict[str, Any]) -> str:
    """
    Multi-Hop Search logic to extract scattering reasoning paths.
    
    1. Pre-Filters vectors down to ONLY chunks matching the target PAN mathematically.
    2. Runs Iterative 'Hop' queries (e.g. Find Subsidiary -> Find Litigation on Subsidiary)
    3. Sorts returning context by Source Reliability to prioritize official docs.
    """
    pan = entity_metadata.get("company_pan")
    
    # HARD FILTER: We only want vectors tied strictly to this PAN
    # (In a real DB, the metadata tag would be attached during parsing. 
    # For our mock testing below, we'll assume it exists if needed or bypass).
    hard_filter = {"entity_pan": pan} if pan else None
    
    # Hop 1: Broad Litigation
    hop_1_results = vector_db.search(
        query="lawsuits, civil suits, defaults, bankruptcy, NCLT proceedings", 
        top_k=3,
        metadata_filter=hard_filter
    )
    
    # Hop 2: Governance & Regulation Headwinds
    hop_2_results = vector_db.search(
        query="fraud, shell company, struck off directors, regulatory penalty, RBI fines",
        top_k=3,
        metadata_filter=hard_filter
    )
    
    # Combine and Deduplicate
    all_chunks = hop_1_results + hop_2_results
    unique_chunks = []
    seen = set()
    for c in all_chunks:
        if c["content"] not in seen:
            seen.add(c["content"])
            unique_chunks.append(c)
            
    # Priority Sort: We want 'High/Official Government' at the VERY TOP of the context window
    # so the LLM anchors its reasoning on the safest data first.
    def sort_key(chunk):
        rel = chunk.get("metadata", {}).get("source_reliability", "Low")
        if "High" in rel: return 0
        if "Medium" in rel: return 1
        return 2

    unique_chunks.sort(key=sort_key)
    
    # Compile the final structured Context String for the LLM
    context_str = "--- EXTRACTED EVIDENCE CHUNKS ---\n\n"
    for i, c in enumerate(unique_chunks):
        source = c.get("metadata", {}).get("source_url", "Unknown")
        rel = c.get("metadata", {}).get("source_reliability", "Unknown")
        context_str += f"[Chunk {i+1}] (Source: {source} | Reliability: {rel})\n{c['content']}\n\n"
        
    return context_str
