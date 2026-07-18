"""
page_modules/performance.py
Deep dive into performance scores: distribution, by-department, by-job-title,
and the relationships that drive performance.
"""

import streamlit as st
from config import COL
from components.kpi_cards import render_kpi_grid
import charts


def render(df):
    st.markdown('<div class="page-title">📈 Performance Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">What drives performance across the organization.</div>',
                unsafe_allow_html=True)

    if df.empty or COL["performance"] not in df.columns:
        st.markdown('<div class="empty-state"><div class="icon">📭</div>No performance data available.</div>',
                    unsafe_allow_html=True)
        return

    render_kpi_grid([
        {"label": "Avg Performance", "value": df[COL["performance"]].mean(), "format": "decimal"},
        {"label": "Median Performance", "value": df[COL["performance"]].median(), "format": "decimal"},
        {"label": "Top Score", "value": df[COL["performance"]].max(), "format": "decimal"},
        {"label": "Std Deviation", "value": df[COL["performance"]].std(), "format": "decimal"},
    ])

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(charts.performance_distribution(df), use_container_width=True)
    with col2:
        st.plotly_chart(charts.performance_category_distribution(df), use_container_width=True)

    st.plotly_chart(charts.avg_performance_by_department(df), use_container_width=True)
    st.plotly_chart(charts.job_title_performance(df), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(charts.training_vs_performance(df), use_container_width=True)
    with col4:
        st.plotly_chart(charts.projects_vs_performance(df), use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(charts.years_vs_performance(df), use_container_width=True)
    with col6:
        st.plotly_chart(charts.overtime_vs_performance(df), use_container_width=True)

    st.markdown('<div class="section-label">TOP &amp; BOTTOM PERFORMERS</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Top 10 Employees", "Bottom 10 Employees"])
    with tab1:
        st.dataframe(charts.top_bottom_employees(df, 10, top=True), use_container_width=True, hide_index=True)
    with tab2:
        st.dataframe(charts.top_bottom_employees(df, 10, top=False), use_container_width=True, hide_index=True)
