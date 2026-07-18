"""
page_modules/salary.py
Compensation analytics: distribution, department comparison, and its
relationship to performance.
"""

import streamlit as st
from config import COL
from components.kpi_cards import render_kpi_grid
import charts


def render(df):
    st.markdown('<div class="page-title">💰 Salary Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Compensation patterns across departments and roles.</div>',
                unsafe_allow_html=True)

    if df.empty or COL["salary"] not in df.columns:
        st.markdown('<div class="empty-state"><div class="icon">📭</div>No salary data available.</div>',
                    unsafe_allow_html=True)
        return

    render_kpi_grid([
        {"label": "Avg Monthly Salary", "value": df[COL["salary"]].mean(), "format": "currency"},
        {"label": "Median Salary", "value": df[COL["salary"]].median(), "format": "currency"},
        {"label": "Highest Salary", "value": df[COL["salary"]].max(), "format": "currency"},
        {"label": "Salary Std Dev", "value": df[COL["salary"]].std(), "format": "currency"},
    ])

    st.plotly_chart(charts.salary_distribution(df), use_container_width=True)
    st.plotly_chart(charts.avg_salary_by_department(df), use_container_width=True)
    st.plotly_chart(charts.salary_vs_performance(df), use_container_width=True)

    if COL["department"] in df.columns:
        st.markdown('<div class="section-label">DEPARTMENT COMPARISON</div>', unsafe_allow_html=True)
        depts = sorted(df[COL["department"]].dropna().unique().tolist())
        c1, c2 = st.columns(2)
        with c1:
            dept_a = st.selectbox("Department A", depts, index=0, key="sal_dept_a")
        with c2:
            dept_b = st.selectbox("Department B", depts, index=min(1, len(depts) - 1), key="sal_dept_b")

        a_avg = df[df[COL["department"]] == dept_a][COL["salary"]].mean()
        b_avg = df[df[COL["department"]] == dept_b][COL["salary"]].mean()
        c3, c4 = st.columns(2)
        with c3:
            st.metric(dept_a, f"₹{a_avg:,.0f}")
        with c4:
            st.metric(dept_b, f"₹{b_avg:,.0f}", delta=f"₹{b_avg - a_avg:,.0f} vs {dept_a}")
