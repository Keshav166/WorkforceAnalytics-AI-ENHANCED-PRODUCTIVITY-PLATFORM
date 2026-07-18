"""
page_modules/satisfaction.py
Employee satisfaction analytics and its relationship to performance and
resignation risk.
"""

import streamlit as st
from config import COL
from components.kpi_cards import render_kpi_grid
import charts


def render(df):
    st.markdown('<div class="page-title">😊 Satisfaction Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">How employees feel, and how that connects to performance and retention.</div>',
                unsafe_allow_html=True)

    if df.empty or COL["satisfaction"] not in df.columns:
        st.markdown('<div class="empty-state"><div class="icon">📭</div>No satisfaction data available.</div>',
                    unsafe_allow_html=True)
        return

    cards = [
        {"label": "Avg Satisfaction", "value": df[COL["satisfaction"]].mean(), "format": "decimal"},
        {"label": "Median Satisfaction", "value": df[COL["satisfaction"]].median(), "format": "decimal"},
    ]
    if COL["resigned"] in df.columns:
        cards.append({"label": "Resignation Rate", "value": df[COL["resigned"]].mean() * 100, "format": "percent"})
    render_kpi_grid(cards)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(charts.satisfaction_distribution(df), use_container_width=True)
    with col2:
        st.plotly_chart(charts.satisfaction_vs_performance(df), use_container_width=True)

    if COL["department"] in df.columns:
        agg = df.groupby(COL["department"])[COL["satisfaction"]].mean().sort_values().reset_index()
        import plotly.express as px
        from config import COLORS
        fig = px.bar(agg, x=COL["satisfaction"], y=COL["department"], orientation="h",
                     title="Average Satisfaction by Department", text_auto=".2f")
        fig.update_traces(marker_color=COLORS["success"])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    if COL["resigned"] in df.columns:
        st.markdown('<div class="section-label">SATISFACTION vs RESIGNATION</div>', unsafe_allow_html=True)
        import plotly.express as px
        fig = px.box(df, x=COL["resigned"], y=COL["satisfaction"],
                     title="Satisfaction Score by Resignation Status",
                     labels={COL["resigned"]: "Resigned (0=No, 1=Yes)"})
        st.plotly_chart(fig, use_container_width=True)
