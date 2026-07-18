"""
utils/filters.py
Builds the professional filter panel (rendered in the sidebar) and applies the
selected filters to the working dataframe. Every chart in the app consumes the
already-filtered dataframe, so filters are computed once per run.
"""

import streamlit as st
from config import COL


def render_filters(df) -> dict:
    """Renders filter widgets in the sidebar and returns the selected values."""
    st.markdown('<div class="filter-panel-title">FILTERS</div>', unsafe_allow_html=True)

    selections = {}

    def multiselect(label, col_key, key):
        if COL[col_key] not in df.columns:
            return None
        options = sorted(df[COL[col_key]].dropna().unique().tolist())
        return st.multiselect(label, options, default=[], key=key,
                               placeholder="All")

    selections["department"] = multiselect("Department", "department", "f_dept")
    selections["gender"] = multiselect("Gender", "gender", "f_gender")
    selections["education"] = multiselect("Education", "education", "f_edu")
    selections["job_title"] = multiselect("Job Title", "job_title", "f_job")
    selections["performance_category"] = multiselect(
        "Performance Category", "performance_category", "f_perf_cat")
    selections["remote_freq"] = multiselect(
        "Remote Work Frequency", "remote_freq", "f_remote")

    if COL["age"] in df.columns:
        a_min, a_max = int(df[COL["age"]].min()), int(df[COL["age"]].max())
        selections["age_range"] = st.slider("Age Range", a_min, a_max, (a_min, a_max), key="f_age")
    if COL["years_at_company"] in df.columns:
        y_min, y_max = float(df[COL["years_at_company"]].min()), float(df[COL["years_at_company"]].max())
        selections["years_range"] = st.slider("Years at Company", y_min, y_max, (y_min, y_max), key="f_years")
    if COL["salary"] in df.columns:
        s_min, s_max = float(df[COL["salary"]].min()), float(df[COL["salary"]].max())
        selections["salary_range"] = st.slider("Salary Range", s_min, s_max, (s_min, s_max),
                                                format="₹%.0f", key="f_salary")

    if st.button("Reset Filters", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k.startswith("f_"):
                del st.session_state[k]
        st.rerun()

    return selections


def apply_filters(df, selections: dict):
    """Applies the selected filter values to the dataframe."""
    filtered = df.copy()

    def apply_multi(col_key, sel_key):
        vals = selections.get(sel_key)
        if vals and COL[col_key] in filtered.columns:
            return filtered[filtered[COL[col_key]].isin(vals)]
        return filtered

    filtered = apply_multi("department", "department")
    filtered = apply_multi("gender", "gender")
    filtered = apply_multi("education", "education")
    filtered = apply_multi("job_title", "job_title")
    filtered = apply_multi("performance_category", "performance_category")
    filtered = apply_multi("remote_freq", "remote_freq")

    if selections.get("age_range") and COL["age"] in filtered.columns:
        lo, hi = selections["age_range"]
        filtered = filtered[(filtered[COL["age"]] >= lo) & (filtered[COL["age"]] <= hi)]

    if selections.get("years_range") and COL["years_at_company"] in filtered.columns:
        lo, hi = selections["years_range"]
        filtered = filtered[(filtered[COL["years_at_company"]] >= lo) & (filtered[COL["years_at_company"]] <= hi)]

    if selections.get("salary_range") and COL["salary"] in filtered.columns:
        lo, hi = selections["salary_range"]
        filtered = filtered[(filtered[COL["salary"]] >= lo) & (filtered[COL["salary"]] <= hi)]

    return filtered
