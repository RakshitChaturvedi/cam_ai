from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Dict, Any, List
import json

def chunk_document(rag_object: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Dual-path text splitter.
    Preserves tables (mocked B-I-IB logic) and chunks standard text 
    using Langchain's RecursiveCharacterTextSplitter.
    """
    content = rag_object.get("content", "")
    metadata = rag_object.get("metadata", {})
    doc_id = rag_object.get("doc_id", "unknown")

    chunks = []
    
    # Simple heuristic to detect if this is a table vs standard text
    # In a full production system this would use a layout parser (like LayoutLM)
    is_table = "TABLE_START" in content or "|" in content
    
    if is_table:
        # Spatial-Aware Mock Logic (B-I-IB tagging preservation)
        # We assume the scraper/normalizer has already structured the table 
        # so we don't sever the rows. We chunk row-by-row conceptually here.
        # For this prototype, we'll just treat the whole table as 1 safe chunk.
        chunks.append({
            "chunk_id": f"{doc_id}_chunk_0_table",
            "content": content,
            "metadata": metadata,
            "chunk_type": "spatial_table"
        })
    else:
        # Standard Text Splitting
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
        )
        
        raw_chunks = text_splitter.split_text(content)
        
        for i, raw_chunk in enumerate(raw_chunks):
            chunks.append({
                "chunk_id": f"{doc_id}_chunk_{i}",
                "content": raw_chunk,
                "metadata": metadata,  # We strictly preserve the parent metadata!
                "chunk_type": "standard_text"
            })
            
    return chunks
