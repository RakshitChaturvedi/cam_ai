from .gst_parser import parse_gst_file
from .bank_statement_parser import parse_bank_statement
from .itr_parser import parse_itr_file
from .financial_normalizer import normalize_financial_data

def process_structured_data(gst_file, bank_file, itr_file):
    gst_data = parse_gst_file(gst_file)
    bank_data = parse_bank_statement(bank_file)
    itr_data = parse_itr_file(itr_file)

    financial_summary = normalize_financial_data(gst_data, bank_data, itr_data)

    return {
        "financial_summary": financial_summary
    }