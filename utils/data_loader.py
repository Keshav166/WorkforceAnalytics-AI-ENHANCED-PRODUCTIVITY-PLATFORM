"""
utils/data_loader.py
Handles loading, cleaning, and caching the employee dataset. Ensures engineered
columns (Tenure_Years, Performance_Category, Overtime_Category) exist even if
the uploaded CSV doesn't already include them.
"""

import os
import pandas as pd
import streamlit as st

from config import DEFAULT_DATA_PATH, COL


def _engineer_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Adds engineered columns if they are missing from the raw dataset."""
    df = df.copy()

    if COL["hire_date"] in df.columns:
        df[COL["hire_date"]] = pd.to_datetime(df[COL["hire_date"]], errors="coerce")

    if COL["tenure_years"] not in df.columns:
        if COL["years_at_company"] in df.columns:
            df[COL["tenure_years"]] = df[COL["years_at_company"]]
        elif COL["hire_date"] in df.columns:
            df[COL["tenure_years"]] = (
                (pd.Timestamp.now() - df[COL["hire_date"]]).dt.days / 365.25
            ).round(2)

    if COL["performance_category"] not in df.columns and COL["performance"] in df.columns:
        perf_max = df[COL["performance"]].max()
        # Thresholds scale relative to the observed max (supports 1-5 or 1-10 style scores)
        def _perf_cat(score):
            if pd.isna(score):
                return "Unknown"
            ratio = score / perf_max if perf_max else 0
            if ratio >= 0.85:
                return "Excellent"
            elif ratio >= 0.65:
                return "Good"
            elif ratio >= 0.45:
                return "Average"
            return "Needs Improvement"
        df[COL["performance_category"]] = df[COL["performance"]].apply(_perf_cat)

    if COL["overtime_category"] not in df.columns and COL["overtime"] in df.columns:
        ot_max = df[COL["overtime"]].max()
        low_cut = ot_max * 0.2
        mod_cut = ot_max * 0.55
        def _ot_cat(hours):
            if pd.isna(hours):
                return "Unknown"
            if hours < low_cut:
                return "Low"
            elif hours < mod_cut:
                return "Moderate"
            return "High"
        df[COL["overtime_category"]] = df[COL["overtime"]].apply(_ot_cat)

    return df


@st.cache_data(show_spinner=False)
def load_data(path: str = None) -> pd.DataFrame:
    """Loads the dataset from disk (or an uploaded file path) and engineers columns."""
    path = path or DEFAULT_DATA_PATH
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    df = _engineer_columns(df)
    return df


def load_uploaded(file) -> pd.DataFrame:
    """Loads a dataset from an uploaded file-like object (Settings page)."""
    df = pd.read_csv(file)
    df = _engineer_columns(df)
    return df


def kpi_summary(df: pd.DataFrame) -> dict:
    """Computes the top-line KPI values shown across the dashboard."""
    if df.empty:
        return {}

    resigned_rate = (
        df[COL["resigned"]].mean() * 100 if COL["resigned"] in df.columns else None
    )
    top_dept = (
        df.groupby(COL["department"])[COL["performance"]].mean().idxmax()
        if COL["department"] in df.columns and COL["performance"] in df.columns
        else "N/A"
    )

    return {
        "total_employees": len(df),
        "avg_performance": df[COL["performance"]].mean() if COL["performance"] in df.columns else None,
        "avg_salary": df[COL["salary"]].mean() if COL["salary"] in df.columns else None,
        "avg_satisfaction": df[COL["satisfaction"]].mean() if COL["satisfaction"] in df.columns else None,
        "avg_training": df[COL["training_hours"]].mean() if COL["training_hours"] in df.columns else None,
        "avg_overtime": df[COL["overtime"]].mean() if COL["overtime"] in df.columns else None,
        "resignation_rate": resigned_rate,
        "top_department": top_dept,
    }
