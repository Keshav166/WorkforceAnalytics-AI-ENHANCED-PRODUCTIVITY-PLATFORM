"""
config.py
Central configuration for the AI-Enhanced Employee Productivity Analytics Dashboard.
Holds design tokens, file paths, column name constants, and app-wide settings so
every other module reads from a single source of truth.
"""

import os

# ----------------------------------------------------------------------------
# PATHS
# ----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DEFAULT_DATA_PATH = os.path.join(DATA_DIR, "employee_data.csv")
STYLE_CSS_PATH = os.path.join(ASSETS_DIR, "style.css")

# ----------------------------------------------------------------------------
# APP METADATA
# ----------------------------------------------------------------------------
APP_TITLE = "AI-Enhanced Employee Productivity Analytics Dashboard"
APP_ICON = "📊"
PAGE_LAYOUT = "wide"

# ----------------------------------------------------------------------------
# DESIGN TOKENS  ("Terminal, modernized" visual language)
# A graphite/ink base with a signal-teal accent and an amber warning tone.
# Numeric/KPI text uses a monospace face to read like live market data;
# headers use a geometric display face; body copy uses a humanist sans.
# ----------------------------------------------------------------------------
COLORS = {
    "bg_primary": "#0A0E14",
    "bg_secondary": "#10161F",
    "bg_card": "#141B26",
    "bg_card_hover": "#182130",
    "border": "#232D3D",
    "border_soft": "#1A2230",
    "text_primary": "#E9EDF4",
    "text_secondary": "#8B98AC",
    "text_muted": "#5B6577",
    "accent": "#00D9B5",       # signal teal — primary accent
    "accent_soft": "#00D9B522",
    "accent_alt": "#5B8CFF",   # secondary blue — links / info
    "warning": "#F5A623",      # amber — warnings / overtime
    "danger": "#FF5C7A",       # rose — negative deltas / resignation
    "success": "#3DDC97",
    "chart_sequence": ["#00D9B5", "#5B8CFF", "#F5A623", "#FF5C7A", "#B26BFF",
                        "#3DDC97", "#FF9F6E", "#6EC6FF"],
}

FONT_DISPLAY = "'Space Grotesk', 'Segoe UI', sans-serif"
FONT_BODY = "'Inter', 'Segoe UI', sans-serif"
FONT_MONO = "'JetBrains Mono', 'Consolas', monospace"

PLOTLY_TEMPLATE = "productivity_dark"

# ----------------------------------------------------------------------------
# DATASET COLUMN NAMES
# ----------------------------------------------------------------------------
COL = {
    "id": "Employee_ID",
    "department": "Department",
    "gender": "Gender",
    "age": "Age",
    "job_title": "Job_Title",
    "hire_date": "Hire_Date",
    "years_at_company": "Years_At_Company",
    "education": "Education_Level",
    "performance": "Performance_Score",
    "salary": "Monthly_Salary",
    "work_hours": "Work_Hours_Per_Week",
    "projects": "Projects_Handled",
    "overtime": "Overtime_Hours",
    "sick_days": "Sick_Days",
    "remote_freq": "Remote_Work_Frequency",
    "team_size": "Team_Size",
    "training_hours": "Training_Hours",
    "promotions": "Promotions",
    "satisfaction": "Employee_Satisfaction_Score",
    "resigned": "Resigned",
    "tenure_years": "Tenure_Years",
    "performance_category": "Performance_Category",
    "overtime_category": "Overtime_Category",
}

# ----------------------------------------------------------------------------
# NAVIGATION
# ----------------------------------------------------------------------------
NAV_ITEMS = [
    ("Overview", "🏠"),
    ("Performance Analytics", "📈"),
    ("Salary Analytics", "💰"),
    ("Department Analysis", "🏢"),
    ("Satisfaction Analysis", "😊"),
    ("Training Analysis", "🎓"),
    ("Remote Work Analysis", "🌍"),
    ("Correlation Matrix", "📊"),
    ("AI Executive Insights", "🤖"),
    ("Settings", "⚙"),
]

# ----------------------------------------------------------------------------
# GEMINI
# ----------------------------------------------------------------------------
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_API_KEY_ENV = "GEMINI_API_KEY"
