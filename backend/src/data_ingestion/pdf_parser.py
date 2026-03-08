import pymupdf
import os

from .document_profiles import DOCUMENT_KEYWORDS
from .document_classifier import detect_document_type
from .signal_extractor import extract_signals_from_chunk

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

    return "\n".join(relevant_text)

def chunk_text(text):
    """
        Split text into chunks for LLM processing.
    """
    chunk_size = len(text)//25
    chunks = []
    start = 0
    
    while start < len(text):
        chunks.append(text[start:start+chunk_size])
        start+=chunk_size

    return chunks

def parse_pdf(pdf_path):
    pages = extract_text_from_pdf(pdf_path)
    doc_type = detect_document_type(pages)
    filtered_text = filter_relevant_pages(pages, doc_type)
    print("Filtered text length:", len(filtered_text))
    
    chunks = chunk_text(filtered_text)
    results = []

    for chunk in chunks:
        signals = extract_signals_from_chunk(chunk, doc_type)
        print("LLM Output:", signals)
        results.append(signals)
    
    return {
        "document_type": doc_type,
        "signals": results
    }

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(__file__)
    test_pdf = os.path.join(BASE_DIR, "data", "sample_annual_report.pdf")

    if os.path.exists(test_pdf):
        result = parse_pdf(test_pdf)
        print("Document Type:", result["document_type"])
        print("\nExtracted Signals:\n")

        for r in result["signals"]:
            print(r)
    else:
        print(f"Error: Please place a PDF at {test_pdf} to test.")
        exit()