"""
components/sidebar.py
Renders the sidebar: brand header, page navigation, dataset upload control,
and the filter panel (from utils.filters).
"""

import streamlit as st
from config import NAV_ITEMS
from utils.filters import render_filters


def render_sidebar(df):
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-brand">Workforce<span>Analytics</span><br>'
            '<span style="font-size:0.68rem;color:var(--text-muted);font-weight:500;'
            'letter-spacing:0.06em;">AI-ENHANCED PRODUCTIVITY PLATFORM</span></div>',
            unsafe_allow_html=True,
        )

        labels = [f"{icon}  {name}" for name, icon in NAV_ITEMS]
        choice = st.radio("Navigate", labels, label_visibility="collapsed", key="nav_choice")
        page = choice.split("  ", 1)[1]

        st.markdown("---")

        selections = render_filters(df) if not df.empty else {}

        return page, selections
