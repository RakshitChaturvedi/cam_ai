## Input

The unstructured pipeline processes financial documents in PDF format.

Accepted inputs:

```text
Annual Reports (.pdf)
Legal Notices (.pdf)
Bank Sanction Letters (.pdf)
```

Example input list:

```python
[
 "data/sample_annual_report.pdf",
 "data/sample_legal_notice.pdf",
 "data/sample_sanction_letter.pdf"
]
```

---

## Code Modules

### document_classifier.py

**Purpose**

Detects the document type.

**Input**

```python
text: str
```

**Output**

```python
"annual_report" | "legal_notice" | "sanction_letter"
```

---

### document_profiles.py

**Purpose**

Stores keyword profiles for each document type.

Used by:

```
classifier
page filter
signal extractor
```

---

### pdf_parser.py

**Purpose**

Main ingestion module.

Steps:

```
PDF → text extraction → classification → filtering → chunking
```

**Input**

```python
pdf_path: str
```

**Output**

```python
{
 "document_type": "...",
 "signals": {...}
}
```

---

### signal_extractor.py

**Purpose**

Uses LLM to extract financial signals.

Example signals:

```
contingent liabilities
debt covenants
capital commitments
```

---


### Key Financial Signals Extracted

The unstructured ingestion pipeline extracts **risk-related financial signals** from documents.
These signals are grouped by document type.

---

## 1. Annual Reports

Annual reports contain disclosures in:

* Notes to Financial Statements
* Auditor Reports
* Risk Disclosures

Key signals extracted:

```text
contingent_liabilities
capital_commitments
corporate_guarantees
related_party_transactions
going_concern_issues
debt_covenants
impairments
receivable_aging_risks
```

### Explanation

| Field                      | Meaning                                         |
| -------------------------- | ----------------------------------------------- |
| Contingent Liabilities     | Potential obligations not yet recorded as debt  |
| Capital Commitments        | Future investments or contractual spending      |
| Corporate Guarantees       | Company guarantees debt of another entity       |
| Related Party Transactions | Financial activity with promoter-owned entities |
| Going Concern Issues       | Auditor doubts about company's survival         |
| Debt Covenants             | Loan conditions tied to financial ratios        |
| Impairments                | Permanent asset value reduction                 |
| Receivable Aging Risks     | Unpaid or disputed receivables                  |

---

## 2. Legal Notices

Legal notices reveal **financial distress or disputes**.

Key signals extracted:

```text
default_events
insolvency_references
section_138_cases
arbitration_disputes
contract_termination
liquidated_damages
garnishee_orders
```

### Explanation

| Field                 | Meaning                                      |
| --------------------- | -------------------------------------------- |
| Default Events        | Failure to meet loan obligations             |
| Insolvency References | Mentions of IBC or NCLT proceedings          |
| Section 138 Cases     | Cheque bounce criminal cases                 |
| Arbitration Disputes  | Commercial disputes under arbitration        |
| Contract Termination  | Contracts cancelled due to breach            |
| Liquidated Damages    | Predefined penalties for project delays      |
| Garnishee Orders      | Court order seizing funds from bank accounts |

---

## 3. Bank Sanction Letters

Sanction letters define **loan conditions and lender protections**.

Key signals extracted:

```text
financial_covenants
cross_default_clauses
material_adverse_change
right_to_setoff
promoter_guarantee
negative_lien
```

### Explanation

| Field                   | Meaning                                               |
| ----------------------- | ----------------------------------------------------- |
| Financial Covenants     | Required financial ratios (DSCR, Current Ratio, etc.) |
| Cross Default           | Default on another loan triggers default here         |
| Material Adverse Change | Bank may recall loan if borrower condition worsens    |
| Right to Set-off        | Bank can seize balances from borrower accounts        |
| Promoter Guarantee      | Personal guarantee from promoters                     |
| Negative Lien           | Borrower cannot pledge assets to other lenders        |

---

### Why These Signals Matter

These signals represent **financial risk indicators** used in credit underwriting.

Examples:

```text
Contingent liabilities → hidden debt exposure
Related party transactions → possible fund diversion
Cross-default clause → systemic credit risk
Section 138 cases → liquidity crisis
```

These extracted signals become input to the **credit risk analysis system**.

---

### signal_aggregator.py

**Purpose**

Merges signals extracted from multiple text chunks.

Example:

```python
[
 {"capital_commitments": "..."},
 {"capital_commitments": "..."}
]
```

↓

```python
{
 "capital_commitments": [...]
}
```

---

### signal_normalizer.py

**Purpose**

Standardizes signal format.

Output example:

```json
{
 "description": "...",
 "source": "annual_report"
}
```

---

### document_processor.py

**Purpose**

Processes multiple documents.

Input:

```python
list[str]
```

Output:

```json
{
 "annual_report": {...},
 "legal_notice": {...},
 "sanction_letter": {...}
}
```

---

# Final Output Format

```json
{
 "annual_report": {
   "capital_commitments": [
     {
       "description": "...",
       "source": "annual_report"
     }
   ]
 },
 "legal_notice": {...},
 "sanction_letter": {...}
}
```

## Example output

```json
{
  "legal_notice": {
    "default_events": [
      {
        "description": "failure to repay outstanding principal amount of \u20b94,75,00,000",
        "source": "legal_notice"
      },
      {
        "description": "failure to pay accrued interest",
        "source": "legal_notice"
      }
    ],
    "insolvency_references": [
      {
        "description": "initiation of proceedings before the National Company Law Tribunal (NCLT) under the Insolvency and Bankruptcy Code",
        "source": "legal_notice"
      }
    ],
    "arbitration_disputes": [
      {
        "description": "pursuit of arbitration as per the dispute resolution clause of the loan agreement",
        "source": "legal_notice"
      }
    ]
  },
  "sanction_letter": {
    "financial_covenants": [
      {
        "description": "Total Outside Liabilities to Tangible Net Worth (TOL/TNW) not exceeding 2.50",
        "source": "sanction_letter"
      },
      {
        "description": "Debt Service Coverage Ratio (DSCR) of not less than 1.25",
        "source": "sanction_letter"
      },
      {
        "description": "Current Ratio not less than 1.33",
        "source": "sanction_letter"
      }
    ],
    "cross_default_clauses": [
      {
        "description": "Default under any other credit facility with any lender constitutes a cross-default",
        "source": "sanction_letter"
      }
    ],
    "material_adverse_change": [
      {
        "description": "Bank reserves the right to recall the loan in case of material adverse change in borrower's financial condition",
        "source": "sanction_letter"
      }
    ],
    "right_to_setoff": [
      {
        "description": "Bank has the right to set-off and adjust any credit balance in borrower's account",
        "source": "sanction_letter"
      }
    ],
    "promoter_guarantee": [
      {
        "description": "Loan facility is secured by a personal guarantee from the company's promoters",
        "source": "sanction_letter"
      }
    ],
    "negative_lien": [
      {
        "description": "Borrower cannot create any charge or security interest over its assets without prior written consent of the bank",
        "source": "sanction_letter"
      }
    ]
  }
}
```
---
