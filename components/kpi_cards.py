"""
components/kpi_cards.py
Renders the animated top-of-page KPI card grid used on the Overview page
(and reused, subset, on other analysis pages).
"""

import streamlit as st


def _format_value(value, fmt):
    if value is None:
        return "—"
    if fmt == "currency":
        return f"₹{value:,.0f}"
    if fmt == "percent":
        return f"{value:.1f}%"
    if fmt == "decimal":
        return f"{value:.2f}"
    if fmt == "int":
        return f"{int(value):,}"
    return str(value)


def render_kpi_grid(cards: list):
    """
    cards: list of dicts, each with keys:
      label (str), value (number), format ("currency"|"percent"|"decimal"|"int"|"text"),
      delta (optional str, e.g. "+4.2%"), delta_dir ("up"|"down"|"neutral")
    """
    html = ['<div class="kpi-grid">']
    for i, card in enumerate(cards):
        value_display = _format_value(card.get("value"), card.get("format", "text"))
        delta_html = ""
        if card.get("delta"):
            direction = card.get("delta_dir", "neutral")
            arrow = {"up": "▲", "down": "▼", "neutral": "●"}[direction]
            delta_html = f'<div class="kpi-delta {direction}">{arrow} {card["delta"]}</div>'
        card_html = (
            f'<div class="kpi-card" style="animation-delay:{i * 0.05}s">'
            f'<div class="kpi-label">{card["label"]}</div>'
            f'<div class="kpi-value">{value_display}</div>'
            f'{delta_html}'
            f'</div>'
        )
        html.append(card_html)
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)
