"""
page_modules/department.py
Cross-metric department comparison view.
"""

import streamlit as st
import pandas as pd
from config import COL
import charts


def render(df):
    st.markdown('<div class="page-title">🏢 Department Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Headcount, performance, and pay side by side, by department.</div>',
                unsafe_allow_html=True)

    if df.empty or COL["department"] not in df.columns:
        st.markdown('<div class="empty-state"><div class="icon">📭</div>No department data available.</div>',
                    unsafe_allow_html=True)
        return

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(charts.department_distribution(df), use_container_width=True)
    with col2:
        st.plotly_chart(charts.avg_performance_by_department(df), use_container_width=True)

    st.plotly_chart(charts.avg_salary_by_department(df), use_container_width=True)

    agg_cols = {}
    for key, label in [("performance", "Avg Performance"), ("salary", "Avg Salary"),
                        ("satisfaction", "Avg Satisfaction"), ("overtime", "Avg Overtime"),
                        ("training_hours", "Avg Training Hrs")]:
        if COL[key] in df.columns:
            agg_cols[COL[key]] = "mean"

    if agg_cols:
        st.markdown('<div class="section-label">DEPARTMENT SCORECARD</div>', unsafe_allow_html=True)
        summary = df.groupby(COL["department"]).agg(agg_cols)
        summary["Headcount"] = df.groupby(COL["department"]).size()
        summary = summary.round(2).sort_values("Headcount", ascending=False)
        st.dataframe(summary, use_container_width=True)
