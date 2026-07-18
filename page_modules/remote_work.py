"""
page_modules/remote_work.py
Remote work frequency analytics: adoption and its relationship to performance
and satisfaction.
"""

import streamlit as st
import plotly.express as px
from config import COL, COLORS
from components.kpi_cards import render_kpi_grid
import charts


def render(df):
    st.markdown('<div class="page-title">🌍 Remote Work Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">How remote work frequency relates to performance and satisfaction.</div>',
                unsafe_allow_html=True)

    if df.empty or COL["remote_freq"] not in df.columns:
        st.markdown('<div class="empty-state"><div class="icon">📭</div>No remote work data available.</div>',
                    unsafe_allow_html=True)
        return

    render_kpi_grid([
        {"label": "Avg Remote Frequency", "value": df[COL["remote_freq"]].mean(), "format": "percent"},
        {"label": "Fully Remote Share",
         "value": (df[COL["remote_freq"]] == 100).mean() * 100 if 100 in df[COL["remote_freq"]].values else 0,
         "format": "percent"},
    ])

    col1, col2 = st.columns(2)
    with col1:
        counts = df[COL["remote_freq"]].value_counts().sort_index().reset_index()
        counts.columns = ["Remote %", "Count"]
        fig = px.bar(counts, x="Remote %", y="Count", title="Remote Work Frequency Distribution", text="Count")
        fig.update_traces(marker_color=COLORS["accent"])
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.plotly_chart(charts.remote_work_analysis(df), use_container_width=True)

    if COL["satisfaction"] in df.columns:
        agg = df.groupby(COL["remote_freq"])[COL["satisfaction"]].mean().sort_index().reset_index()
        fig = px.line(agg, x=COL["remote_freq"], y=COL["satisfaction"], markers=True,
                      title="Average Satisfaction by Remote Work Frequency")
        fig.update_traces(line_color=COLORS["success"], marker_color=COLORS["success"])
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)
