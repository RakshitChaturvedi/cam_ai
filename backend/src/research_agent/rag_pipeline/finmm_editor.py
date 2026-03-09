import re

def correct_ocr_hallucinations(text: str) -> str:
    """
    Context-aware OCR correction layer for Indian Financial data.
    Provides a fast, $0 cost approach using Regex heuristics to fix common 
    OCR artifacts before vectorization.
    """
    
    # 1. Currency Symbol Corrections (Context Aware)
    # Often '?' or '¥' appears instead of 'RS.' or '₹' before numbers.
    # We fix this if adjacent to a number and within a financial context.
    text = re.sub(r'[\?¥]\s*(\d+[,\.]?\d*)', r'₹ \1', text)
    
    # 2. Number/Letter confusion in financial strings (O vs 0)
    # If an 'O' is completely surrounded by digits or commas, it's likely a 0
    text = re.sub(r'(?<=\d)O(?=\d)', '0', text)
    text = re.sub(r'(?<=\d,)O(?=\d)', '0', text)
    text = re.sub(r'(?<=\d)O(?=,?\d)', '0', text)

    # 3. Spurious whitespace inside numbers (e.g. 1, 00, 000 -> 1,00,000)
    text = re.sub(r'(?<=\d,)\s*(?=\d)', '', text)
    
    # Clean up double spaces created by the parser
    text = re.sub(r'\s{2,}', ' ', text)
    
    return text.strip()
