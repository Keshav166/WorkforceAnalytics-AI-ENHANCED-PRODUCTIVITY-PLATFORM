"""
ai.py
Handles all communication with the Google Gemini API for the
"AI Executive Insights" page: builds a data-grounded prompt from the current
KPI/filter context and parses the model's structured response.
"""

import os
import json
import streamlit as st

from config import GEMINI_MODEL, GEMINI_API_KEY_ENV

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


def get_api_key() -> str:
    """Resolves the Gemini API key from Streamlit secrets or environment variables."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass  # no secrets.toml configured — fall back to environment variable
    return os.environ.get(GEMINI_API_KEY_ENV, "")


def build_prompt(kpis: dict, dept_summary: str, filters_desc: str) -> str:
    """Builds the analyst prompt sent to Gemini, grounded in the current dashboard state."""
    return f"""
You are a senior workforce analytics consultant preparing an executive report
for a company's leadership team. Base your analysis ONLY on the data summary
below — do not invent numbers.

CURRENT VIEW FILTERS: {filters_desc or "None (full dataset)"}

KEY METRICS:
- Total Employees: {kpis.get('total_employees')}
- Average Performance Score: {kpis.get('avg_performance'):.2f}
- Average Monthly Salary: ₹{kpis.get('avg_salary'):,.0f}
- Average Satisfaction Score: {kpis.get('avg_satisfaction'):.2f}
- Average Training Hours: {kpis.get('avg_training'):.1f}
- Average Overtime Hours: {kpis.get('avg_overtime'):.1f}
- Resignation Rate: {kpis.get('resignation_rate'):.1f}%
- Highest Performing Department: {kpis.get('top_department')}

DEPARTMENT-LEVEL SUMMARY:
{dept_summary}

Write a structured executive report with these exact sections, using markdown
headers (##):
## Executive Summary
## Business Insights
## Risks
## Recommendations
## Future Strategy

Keep it concise, data-driven, and actionable — written for a CHRO/CEO audience.
"""


def generate_report(kpis: dict, dept_summary: str, filters_desc: str) -> str:
    """Calls Gemini and returns the generated report text (or an error message)."""
    api_key = get_api_key()

    if not api_key:
        return (
            "⚠️ No Gemini API key configured. Add `GEMINI_API_KEY` to "
            "`.streamlit/secrets.toml` or as an environment variable to enable "
            "AI-generated reports."
        )

    if not GENAI_AVAILABLE:
        return (
            "⚠️ The `google-genai` package is not installed. Run "
            "`pip install google-genai` and restart the app."
        )

    try:
        client = genai.Client(api_key=api_key)
        prompt = build_prompt(kpis, dept_summary, filters_desc)
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return response.text
    except Exception as exc:
        return f"⚠️ AI report generation failed: {exc}"


def build_department_summary(df, col_map) -> str:
    """Produces a compact per-department table (as text) to ground the AI prompt."""
    if df.empty or col_map["department"] not in df.columns:
        return "No department data available."

    agg_cols = {}
    if col_map["performance"] in df.columns:
        agg_cols[col_map["performance"]] = "mean"
    if col_map["salary"] in df.columns:
        agg_cols[col_map["salary"]] = "mean"
    if col_map["satisfaction"] in df.columns:
        agg_cols[col_map["satisfaction"]] = "mean"
    if col_map["resigned"] in df.columns:
        agg_cols[col_map["resigned"]] = "mean"

    if not agg_cols:
        return "No numeric KPI columns available for department summary."

    summary = df.groupby(col_map["department"]).agg(agg_cols).round(2)
    return summary.to_string()
