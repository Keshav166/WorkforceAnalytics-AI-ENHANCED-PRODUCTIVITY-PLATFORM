"""
utils/styling.py
Injects the custom CSS file into the Streamlit app and registers a shared
Plotly template so every chart in the dashboard shares one visual identity.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

from config import STYLE_CSS_PATH, COLORS, FONT_BODY, PLOTLY_TEMPLATE


def inject_css():
    with open(STYLE_CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def register_plotly_theme():
    """Registers a reusable dark Plotly template matching the CSS design tokens."""
    template = go.layout.Template()
    template.layout = go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_BODY, color=COLORS["text_secondary"], size=12),
        title=dict(font=dict(family=FONT_BODY, size=15, color=COLORS["text_primary"])),
        colorway=COLORS["chart_sequence"],
        xaxis=dict(
            gridcolor=COLORS["border_soft"], zerolinecolor=COLORS["border"],
            linecolor=COLORS["border"], tickfont=dict(color=COLORS["text_secondary"]),
        ),
        yaxis=dict(
            gridcolor=COLORS["border_soft"], zerolinecolor=COLORS["border"],
            linecolor=COLORS["border"], tickfont=dict(color=COLORS["text_secondary"]),
        ),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text_secondary"])),
        margin=dict(l=10, r=10, t=40, b=10),
        hoverlabel=dict(
            bgcolor=COLORS["bg_card"], font=dict(color=COLORS["text_primary"], family=FONT_BODY),
            bordercolor=COLORS["border"],
        ),
    )
    pio.templates[PLOTLY_TEMPLATE] = template
    pio.templates.default = PLOTLY_TEMPLATE
