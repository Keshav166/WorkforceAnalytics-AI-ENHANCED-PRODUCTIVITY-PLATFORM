"""
page_modules/overview.py
The landing page: full KPI grid plus a high-level view of workforce
composition and performance spread.
"""

import streamlit as st
from config import COL
from utils.data_loader import kpi_summary
from components.kpi_cards import render_kpi_grid
import charts


def render(df):
    st.markdown('<div class="page-title">🏠 Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Workforce health at a glance, updated live with your filters.</div>',
                unsafe_allow_html=True)

    if df.empty:
        st.markdown(
            '<div class="empty-state"><div class="icon">📭</div>'
            'No data matches the current filters. Try widening your selection.</div>',
            unsafe_allow_html=True)
        return

    kpis = kpi_summary(df)

    cards = [
        {"label": "Total Employees", "value": kpis.get("total_employees"), "format": "int"},
        {"label": "Avg Performance Score", "value": kpis.get("avg_performance"), "format": "decimal"},
        {"label": "Avg Monthly Salary", "value": kpis.get("avg_salary"), "format": "currency"},
        {"label": "Avg Satisfaction", "value": kpis.get("avg_satisfaction"), "format": "decimal"},
        {"label": "Avg Training Hours", "value": kpis.get("avg_training"), "format": "decimal"},
        {"label": "Avg Overtime Hours", "value": kpis.get("avg_overtime"), "format": "decimal"},
        {"label": "Resignation Rate", "value": kpis.get("resignation_rate"), "format": "percent",
         "delta": "vs. target 10%",
         "delta_dir": "down" if (kpis.get("resignation_rate") or 0) <= 10 else "up"},
        {"label": "Top Department", "value": kpis.get("top_department"), "format": "text"},
    ]
    render_kpi_grid(cards)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(charts.department_distribution(df), use_container_width=True)
    with col2:
        st.plotly_chart(charts.gender_distribution(df), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(charts.performance_distribution(df), use_container_width=True)
    with col4:
        st.plotly_chart(charts.performance_category_distribution(df), use_container_width=True)

    with st.expander("📥 Download filtered dataset"):
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download as CSV", csv, "filtered_employee_data.csv", "text/csv",
                            use_container_width=True)
