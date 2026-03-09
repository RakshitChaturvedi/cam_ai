
---

# Structured Data Ingestion Pipeline

## Input

The structured pipeline processes **financial datasets** exported from accounting systems, GST filings, and tax returns.

Accepted inputs:

```text
GST Filings (.csv / .xlsx)
Bank Statements (.csv / .xlsx)
Income Tax Returns (ITR) (.csv / .xlsx)
```

Example input configuration:

```python
{
 "gst": "data/sample_gst.csv",
 "bank": "data/sample_bank.csv",
 "itr": "data/sample_itr.csv"
}
```

---

# Code Modules

## gst_parser.py

**Purpose**

Parses GST invoice datasets into structured records.

These datasets represent **transaction-level sales data** used for turnover analysis and trading network construction.

**Input**

```python
gst_file: str
```

Example dataset:

```text
invoice_number,seller_gstin,buyer_gstin,amount,date
INV001,27AAA1111A1Z1,27BBB2222B1Z2,500000,2024-01-10
```

**Output**

```python
[
 {
  "seller_gstin": "...",
  "buyer_gstin": "...",
  "amount": 500000,
  "date": "2024-01-10"
 }
]
```

---

## bank_parser.py

**Purpose**

Parses bank statement datasets into structured transaction records.

These records represent **actual cash inflows and outflows**.

**Input**

```python
bank_file: str
```

Example dataset:

```text
date,description,amount,type
2024-01-10,NEFT from Company B,500000,CREDIT
```

**Output**

```python
[
 {
  "date": "2024-01-10",
  "description": "NEFT from Company B",
  "amount": 500000,
  "type": "CREDIT"
 }
]
```

---

## itr_parser.py

**Purpose**

Parses Income Tax Return summaries to extract declared financial income.

**Input**

```python
itr_file: str
```

Example dataset:

```text
assessment_year,total_income,tax_paid
2024,900000,270000
```

**Output**

```python
[
 {
  "assessment_year": 2024,
  "total_income": 900000,
  "tax_paid": 270000
 }
]
```

---

## financial_normalizer.py

**Purpose**

Converts raw financial records into a **unified financial summary**.

This allows downstream detectors to work on standardized financial metrics.

**Input**

```python
gst_records
bank_records
itr_records
```

**Output**

```json
{
 "gst_sales": 2000000,
 "bank_inflows": 1700000,
 "itr_income": 900000
}
```

---

# Financial Signals Extracted

The structured ingestion pipeline detects **financial anomalies and inconsistencies** across datasets.

---

## 1. Circular Trading Detection

Circular trading occurs when companies trade invoices in a loop to artificially inflate turnover.

Example pattern:

```text
Company A → Company B
Company B → Company C
Company C → Company A
```

Detected using **graph cycle detection on GST transactions**.

Fields extracted:

```text
circular_trading_detected
cycles
```

Example output:

```json
{
 "circular_trading_detected": true,
 "cycles": [
  ["27BBB2222B1Z2","27CCC3333C1Z3","27AAA1111A1Z1"]
 ]
}
```

---

## 2. Revenue Mismatch Detection

Compares **GST reported sales** against **bank cash inflows**.

Large discrepancies may indicate:

```text
fake invoicing
channel stuffing
revenue inflation
```

Fields extracted:

```text
gst_sales
bank_inflows
ratio
revenue_inflation_flag
```

Example output:

```json
{
 "gst_sales": 2000000,
 "bank_inflows": 1700000,
 "ratio": 0.85,
 "revenue_inflation_flag": false
}
```

---

## 3. Income Consistency Check

Compares **GST turnover** against **ITR declared income**.

Significant inconsistencies may indicate:

```text
underreported income
aggressive accounting
tax irregularities
```

Fields extracted:

```text
gst_sales
itr_income
income_ratio
income_inconsistency_flag
```

Example output:

```json
{
 "gst_sales": 2000000,
 "itr_income": 900000,
 "income_ratio": 0.45,
 "income_inconsistency_flag": false
}
```

---

# Anomaly Detection Modules

## circular_trading_detector.py

Detects invoice trading cycles using a **directed graph of GST transactions**.

Input:

```python
gst_records
```

Output:

```json
{
 "circular_trading_detected": true,
 "cycles": [...]
}
```

---

## revenue_mismatch_detector.py

Detects discrepancies between **GST sales and bank inflows**.

Input:

```python
gst_records
bank_records
```

Output:

```json
{
 "ratio": 0.85,
 "revenue_inflation_flag": false
}
```

---

## income_consistency_checker.py

Checks consistency between **GST turnover and declared ITR income**.

Input:

```python
gst_records
itr_records
```

Output:

```json
{
 "income_ratio": 0.45,
 "income_inconsistency_flag": false
}
```

---

# structured_data_processor.py

**Purpose**

Main orchestrator for the structured pipeline.

Steps:

```text
GST Parser
↓
Bank Parser
↓
ITR Parser
↓
Financial Normalization
↓
Anomaly Detection
```

**Input**

```python
{
 "gst": "data/sample_gst.csv",
 "bank": "data/sample_bank.csv",
 "itr": "data/sample_itr.csv"
}
```

---

# Final Output Format

```json
{
 "structured_financial_analysis": {
   "financial_summary": {
     "gst_sales": 2000000,
     "bank_inflows": 1700000,
     "itr_income": 900000
   },

   "circular_trading": {...},

   "revenue_mismatch": {...},

   "income_consistency": {...},

   "risk_summary": {
     "circular_trading_risk": true,
     "revenue_mismatch_risk": false,
     "income_inconsistency_risk": false
   }
 }
}
```

---

# Example Output

```json
{
  "structured_financial_analysis": {
    "financial_summary": {
      "gst_sales": 2000000,
      "bank_inflows": 1700000,
      "itr_income": 900000
    },
    "circular_trading": {
      "circular_trading_detected": true,
      "cycles": [
        [
          "27BBB2222B1Z2",
          "27CCC3333C1Z3",
          "27AAA1111A1Z1"
        ]
      ]
    },
    "revenue_mismatch": {
      "gst_sales": 2000000,
      "bank_inflows": 1700000,
      "ratio": 0.85,
      "revenue_inflation_flag": false
    },
    "income_consistency": {
      "gst_sales": 2000000,
      "itr_income": 900000,
      "income_ratio": 0.45,
      "income_inconsistency_flag": false
    },
    "risk_summary": {
      "circular_trading_risk": true,
      "revenue_mismatch_risk": false,
      "income_inconsistency_risk": false
    }
  }
}
```

---
