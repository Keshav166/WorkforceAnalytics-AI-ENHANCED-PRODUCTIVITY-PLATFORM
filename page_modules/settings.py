"""
page_modules/settings.py
App settings: dataset source (default vs. upload), employee search by ID,
theme toggle, and API key status.
"""

import streamlit as st
from config import COL, DEFAULT_DATA_PATH, GEMINI_API_KEY_ENV
from utils.data_loader import load_uploaded
import os


def render(df):
    st.markdown('<div class="page-title">⚙ Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Data source, appearance, and lookups.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">DATA SOURCE</div>', unsafe_allow_html=True)
    st.caption(f"Currently loaded from: `{DEFAULT_DATA_PATH}`")
    uploaded = st.file_uploader("Upload a replacement dataset (CSV)", type=["csv"])
    if uploaded is not None:
        try:
            new_df = load_uploaded(uploaded)
            st.session_state["uploaded_df"] = new_df
            st.success(f"Loaded {len(new_df):,} rows. Switch pages to see it reflected everywhere.")
        except Exception as exc:
            st.error(f"Could not read file: {exc}")

    if "uploaded_df" in st.session_state and st.button("Revert to default dataset"):
        del st.session_state["uploaded_df"]
        st.rerun()

    st.markdown('<div class="section-label">APPEARANCE</div>', unsafe_allow_html=True)
    theme = st.radio("Theme", ["Dark (recommended)", "Light"], horizontal=True,
                      index=0 if st.session_state.get("theme", "dark") == "dark" else 1)
    st.session_state["theme"] = "dark" if theme.startswith("Dark") else "light"
    if st.session_state["theme"] == "light":
        st.info("Light mode is a work in progress in this build — the dashboard is optimized for dark mode.")

    st.markdown('<div class="section-label">EMPLOYEE SEARCH</div>', unsafe_allow_html=True)
    if not df.empty and COL["id"] in df.columns:
        query = st.text_input("Search by Employee ID", placeholder="e.g. EMP100042")
        if query:
            match = df[df[COL["id"]].astype(str).str.contains(query, case=False, na=False)]
            if match.empty:
                st.markdown(
                    '<div class="empty-state"><div class="icon">🔍</div>No employee matches that ID.</div>',
                    unsafe_allow_html=True)
            else:
                st.dataframe(match, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-label">AI CONFIGURATION</div>', unsafe_allow_html=True)
    try:
        secret_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else ""
    except Exception:
        secret_key = ""  # no secrets.toml configured
    key_present = bool(os.environ.get(GEMINI_API_KEY_ENV) or secret_key)
    st.metric("Gemini API Key", "Configured ✅" if key_present else "Not configured ⚠️")
    if not key_present:
        st.caption(
            "Add `GEMINI_API_KEY` to `.streamlit/secrets.toml` or as an environment "
            "variable to enable the AI Executive Insights page."
        )

    st.markdown('<div class="section-label">ABOUT</div>', unsafe_allow_html=True)
    st.caption("AI-Enhanced Employee Productivity Analytics Dashboard · Built with Streamlit, Plotly & Gemini.")
