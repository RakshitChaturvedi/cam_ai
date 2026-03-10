import pymupdf
import json
import os
import time

from .document_profiles import DOCUMENT_KEYWORDS
from .document_classifier import detect_document_type
from .signal_extractor import extract_signals_from_chunk
from .signal_aggregator import aggregate_signals
from .signal_normalizer import normalize_signals

def extract_text_from_pdf(pdf_path):
    """
        Extract raw text from PDF pages.
    """
    doc = pymupdf.open(pdf_path)
    pages = []

    for page_number, page in enumerate(doc):
        text = page.get_text().lower()

        pages.append({
            "page_number": page_number,
            "text": text
        })

        print("Page", page_number, "length:", len(text))


    return pages

def filter_relevant_pages(pages, doc_type):
    keywords = DOCUMENT_KEYWORDS.get(doc_type, [])
    relevant_text = []

    print("Detected doc type: ", doc_type)
    print("Keyword count:", len(keywords))

    for page in pages:
        text = page["text"]

        score = 0

        for keyword in keywords:
            parts = keyword.split()

            if all(p in text for p in parts):
                score += 1

        if score >= 1:
            relevant_text.append(text)
    if not relevant_text:
        print("No keyword pages found")
        relevant_text = [p["text"] for p in pages[:10]]

    return relevant_text

def chunk_text(text_list, max_chunks = 3):
    """
        Split text into chunks for LLM processing.
        text_list can be a list of page texts or a single string.
    """
    if isinstance(text_list, list):
        text = "\n".join(text_list)
    else:
        text = text_list
    
    # Use smaller chunks to stay within Groq free tier TPM limits
    chunk_size = 2000
    chunks = []
    start = 0
    
    while start < len(text) and len(chunks) < max_chunks:
        chunks.append(text[start:start+chunk_size])
        start+=chunk_size

    return chunks

def parse_pdf(pdf_path):
    pages = extract_text_from_pdf(pdf_path)
    doc_type = detect_document_type(pages)
    filtered_text = filter_relevant_pages(pages, doc_type)
    print("Filtered text length:", len(filtered_text), "pages")
    
    chunks = chunk_text(filtered_text)
    results = []

    for chunk in chunks:
        signals = extract_signals_from_chunk(chunk, doc_type)
        time.sleep(0.5)

        try:
            parsed = json.loads(signals)
            results.append(parsed)
        except Exception as e:
            print("JSON parse failed: ", e)
    
    aggregated = aggregate_signals(results)
    normalized = normalize_signals(aggregated, doc_type)
    
    return {
        "document_type": doc_type,
        "signals": normalized
    }