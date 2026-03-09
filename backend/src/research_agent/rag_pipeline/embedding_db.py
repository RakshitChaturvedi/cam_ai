import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

class LocalVectorDB:
    """
    Free $0 cost semantic vector database using FAISS and MiniLM.
    Supports metadata filtering (via secondary indexing).
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Initialize the free, open-source embedding model
        print(f"Loading embedding model {model_name}...")
        self.encoder = SentenceTransformer(model_name)
        
        # MiniLM outputs 384-dimensional vectors
        self.d = 384  
        
        # Initialize FAISS Index (L2 distance)
        self.index = faiss.IndexFlatL2(self.d)
        
        # Since FAISS Flat limits us to just vectors, we need an in-memory 
        # document store to hold the text and metadata for retrieval side-by-side.
        self.doc_store: List[Dict[str, Any]] = []
        
    def add_chunks(self, chunks: List[Dict[str, Any]]):
        if not chunks:
            return
            
        texts = [chunk["content"] for chunk in chunks]
        
        # 1. Generate Embeddings using SentenceTransformers
        embeddings = self.encoder.encode(texts)
        # Convert to float32 as required by FAISS
        faiss_vectors = np.array(embeddings).astype('float32')
        
        # 2. Add vectors to FAISS
        self.index.add(faiss_vectors)
        
        # 3. Add to Document Store (Metadata map)
        self.doc_store.extend(chunks)
        print(f"Added {len(chunks)} chunks to FAISS Index.")
        
        
    def search(self, query: str, top_k: int = 5, metadata_filter: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Retrieves the top_k most similar chunks.
        Applies a post-fetch metadata filter to mimic advanced Pinecone behavior locally.
        """
        # Encode the query
        query_vector = self.encoder.encode([query]).astype('float32')
        
        # We fetch a larger pool (top_k * 5) to allow for aggressive metadata filtering downstream
        fetch_k = top_k * 5 if metadata_filter else top_k
        distances, indices = self.index.search(query_vector, fetch_k)
        
        results = []
        for i, doc_idx in enumerate(indices[0]):
            if doc_idx == -1: # FAISS returns -1 if there are no more vectors
                break
                
            doc = self.doc_store[doc_idx]
            
            # Hardware-Level Metadata Post-Filtering
            passed_filter = True
            if metadata_filter:
                for k, v in metadata_filter.items():
                    # Check if the metadata key exists and matches
                    if doc.get("metadata", {}).get(k) != v:
                        passed_filter = False
                        break
                        
            if passed_filter:
                results.append({
                    "content": doc["content"],
                    "metadata": doc["metadata"],
                    "distance": float(distances[0][i])
                })
                
            # Stop if we hit our requested top_k after filtering
            if len(results) >= top_k:
                break
                
        return results
