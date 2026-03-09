from .gst_parser import parse_gst_file
from .bank_statement_parser import parse_bank_statement
from .itr_parser import parse_itr_file
from .financial_normalizer import normalize_financial_data

from .circular_trading_detector import detect_circular_trading
from .income_consistency_checker import check_income_consistency
from .revenue_mismatch_detector import detect_revenue_mismatch

def process_structured_data(gst_file, bank_file, itr_file):
    gst_data = parse_gst_file(gst_file)
    bank_data = parse_bank_statement(bank_file)
    itr_data = parse_itr_file(itr_file)

    financial_summary = normalize_financial_data(gst_data, bank_data, itr_data)
    circular_trading = detect_circular_trading(gst_data)
    revenue_mismatch = detect_revenue_mismatch(gst_data, bank_data)
    income_consistency = check_income_consistency(gst_data, itr_data)

    risk_summary = {
        "circular_trading_risk": circular_trading["circular_trading_detected"],
        "revenue_mismatch_risk": revenue_mismatch["revenue_inflation_flag"],
        "income_inconsistency_risk": income_consistency["income_inconsistency_flag"]
    }

    return {
        "financial_summary": financial_summary,
        "circular_trading": circular_trading,
        "revenue_mismatch": revenue_mismatch,
        "income_consistency": income_consistency,
        "risk_summary": risk_summary
    }