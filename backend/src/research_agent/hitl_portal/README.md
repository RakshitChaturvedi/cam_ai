# 🧑‍💻 Human-in-the-Loop (HITL) Primary Insight Portal

This module bridges the gap between structured data and human intuition. It allows Credit Officers to log qualitative field notes which are dynamically mapped to a risk framework.

## 📂 Components

- **`nlp_risk_extractor.py`**: Uses Llama-3 (via Groq) to parse unstructured officer notes (e.g., "Factory is understaffed"). It automatically maps the insight to one of the **Five Cs of Credit** (Character, Capacity, Capital, Collateral, Conditions) and assigns a sentiment/severity score.
- **`dynamic_scorer.py`**: A **Deterministic Math Adjuster**. To avoid calculation hallucinations, this script takes the AI-generated sentiment and applies hard-coded mathematical rules to adjust credit scores.
- **`test_hitl.py`**: A simulator to verify the end-to-end flow from a text input to a transparent score adjustment log.

## 📊 Explainablility
Every adjustment made by the HITL Portal generates a transparent **Adjustment Log**. This ensures the final Credit Appraisal Memo (CAM) can explicitly justify its score changes (e.g., "Deducted 8 points from Capacity due to Negative Field Note: Factory underutilization").
