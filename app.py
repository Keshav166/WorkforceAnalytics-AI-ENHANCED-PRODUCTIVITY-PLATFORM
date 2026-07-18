"""
app.py
Entry point for the AI-Enhanced Employee Productivity Analytics Dashboard.
Sets up the page config, loads data, renders the sidebar (nav + filters),
applies filters, and dispatches to the selected page module.
"""

import streamlit as st

from config import APP_TITLE, APP_ICON, PAGE_LAYOUT
from utils.styling import inject_css, register_plotly_theme
from utils.data_loader import load_data
from utils.filters import apply_filters
from components.sidebar import render_sidebar

from page_modules import (
    overview, performance, salary, department,
    satisfaction, training, remote_work, correlation,
    ai_insights, settings,
)

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout=PAGE_LAYOUT,
                    initial_sidebar_state="expanded")

inject_css()
register_plotly_theme()

# ---------------------------------------------------------------- load data
base_df = st.session_state.get("uploaded_df")
if base_df is None:
    base_df = load_data()

# ---------------------------------------------------------------- sidebar (nav + filters)
page, selections = render_sidebar(base_df)

# ---------------------------------------------------------------- apply filters
filtered_df = apply_filters(base_df, selections) if not base_df.empty else base_df

# ---------------------------------------------------------------- route to page
PAGE_MAP = {
    "Overview": lambda: overview.render(filtered_df),
    "Performance Analytics": lambda: performance.render(filtered_df),
    "Salary Analytics": lambda: salary.render(filtered_df),
    "Department Analysis": lambda: department.render(filtered_df),
    "Satisfaction Analysis": lambda: satisfaction.render(filtered_df),
    "Training Analysis": lambda: training.render(filtered_df),
    "Remote Work Analysis": lambda: remote_work.render(filtered_df),
    "Correlation Matrix": lambda: correlation.render(filtered_df),
    "AI Executive Insights": lambda: ai_insights.render(filtered_df, selections),
    "Settings": lambda: settings.render(base_df),
}

if base_df.empty and page != "Settings":
    st.markdown('<div class="page-title">📭 No dataset loaded</div>', unsafe_allow_html=True)
    st.markdown(
        "Place your CSV at `data/employee_data.csv`, or run "
        "`python data/generate_sample_data.py` to create a sample dataset, "
        "or upload one from the **Settings** page."
    )
else:
    PAGE_MAP[page]()
