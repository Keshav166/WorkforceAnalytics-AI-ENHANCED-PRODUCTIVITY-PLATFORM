"""
page_modules/training.py
Training investment analytics and its link to performance outcomes.
"""

import streamlit as st
import plotly.express as px
from config import COL, COLORS
from components.kpi_cards import render_kpi_grid
import charts


def render(df):
    st.markdown('<div class="page-title">🎓 Training Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Where training investment is going, and what it returns.</div>',
                unsafe_allow_html=True)

    if df.empty or COL["training_hours"] not in df.columns:
        st.markdown('<div class="empty-state"><div class="icon">📭</div>No training data available.</div>',
                    unsafe_allow_html=True)
        return

    render_kpi_grid([
        {"label": "Avg Training Hours", "value": df[COL["training_hours"]].mean(), "format": "decimal"},
        {"label": "Max Training Hours", "value": df[COL["training_hours"]].max(), "format": "decimal"},
        {"label": "Total Training Hours", "value": df[COL["training_hours"]].sum(), "format": "int"},
    ])

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(df, x=COL["training_hours"], nbins=25, title="Training Hours Distribution")
        fig.update_traces(marker_color=COLORS["accent"])
        fig.update_layout(height=380, bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.plotly_chart(charts.training_vs_performance(df), use_container_width=True)

    if COL["department"] in df.columns:
        agg = df.groupby(COL["department"])[COL["training_hours"]].mean().sort_values().reset_index()
        fig = px.bar(agg, x=COL["training_hours"], y=COL["department"], orientation="h",
                     title="Average Training Hours by Department", text_auto=".1f")
        fig.update_traces(marker_color=COLORS["accent_alt"])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
