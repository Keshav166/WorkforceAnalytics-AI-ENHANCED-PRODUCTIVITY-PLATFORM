"""
page_modules/correlation.py
Correlation matrix across all numeric workforce metrics, plus an interactive
correlation explorer for any two chosen variables.
"""

import streamlit as st
import plotly.express as px
from config import COL, COLORS
import charts


def render(df):
    st.markdown('<div class="page-title">📊 Correlation Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">How workforce metrics move together.</div>', unsafe_allow_html=True)

    if df.empty:
        st.markdown('<div class="empty-state"><div class="icon">📭</div>No data available.</div>',
                    unsafe_allow_html=True)
        return

    st.plotly_chart(charts.correlation_heatmap(df), use_container_width=True)

    numeric_cols = [c for c in [
        COL["age"], COL["years_at_company"], COL["performance"], COL["salary"],
        COL["work_hours"], COL["projects"], COL["overtime"], COL["sick_days"],
        COL["team_size"], COL["training_hours"], COL["promotions"], COL["satisfaction"],
    ] if c in df.columns]

    if len(numeric_cols) >= 2:
        st.markdown('<div class="section-label">CORRELATION EXPLORER</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            x_var = st.selectbox("Variable X", numeric_cols, index=0, key="corr_x")
        with c2:
            y_var = st.selectbox("Variable Y", numeric_cols,
                                  index=min(1, len(numeric_cols) - 1), key="corr_y")

        r = df[x_var].corr(df[y_var])
        st.metric(f"Correlation ({x_var} vs {y_var})", f"{r:.3f}")

        fig = px.scatter(df, x=x_var, y=y_var, opacity=0.55, trendline="ols",
                          title=f"{x_var} vs {y_var}",
                          color_discrete_sequence=[COLORS["accent"]])
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)
