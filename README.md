# AI-Enhanced Employee Productivity Analytics Dashboard

A production-style Streamlit BI dashboard for the Extended Employee Performance
and Productivity dataset, with Gemini-powered AI Executive Insights.

## Project structure

```
employee_dashboard/
├── app.py                    # Entry point — nav, filters, page routing
├── config.py                 # Design tokens, column map, nav, constants
├── ai.py                     # Gemini integration for AI Executive Insights
├── charts.py                 # All reusable Plotly chart builders
├── requirements.txt
├── data/
│   ├── employee_data.csv     # Your dataset lives here (or upload via Settings)
│   └── generate_sample_data.py  # Synthetic dataset for local dev/demo
├── utils/
│   ├── data_loader.py        # Load/cache/engineer columns, KPI aggregation
│   ├── filters.py            # Sidebar filter widgets + filter application
│   └── styling.py            # CSS injection + shared Plotly dark theme
├── components/
│   ├── kpi_cards.py          # Animated KPI card grid
│   └── sidebar.py            # Brand header, nav, filter panel wiring
└── page_modules/             # One module per sidebar page
    ├── overview.py
    ├── performance.py
    ├── salary.py
    ├── department.py
    ├── satisfaction.py
    ├── training.py
    ├── remote_work.py
    ├── correlation.py
    ├── ai_insights.py
    └── settings.py
```

## Setup

```bash
pip install -r requirements.txt
```

### 1. Add your dataset

Place your CSV at `data/employee_data.csv` with (at least a subset of) these
columns:

```
Employee_ID, Department, Gender, Age, Job_Title, Hire_Date, Years_At_Company,
Education_Level, Performance_Score, Monthly_Salary, Work_Hours_Per_Week,
Projects_Handled, Overtime_Hours, Sick_Days, Remote_Work_Frequency, Team_Size,
Training_Hours, Promotions, Employee_Satisfaction_Score, Resigned
```

Don't have a dataset handy? Generate a realistic synthetic one:

```bash
python data/generate_sample_data.py
```

You can also upload a CSV directly from the **Settings** page at runtime.

### 2. Configure the Gemini API key (for AI Executive Insights)

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

or set an environment variable instead:

```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

The rest of the dashboard works fully without a key — only the AI Executive
Insights page needs it.

### 3. Run

```bash
streamlit run app.py
```

## Notes

- Engineered columns (`Tenure_Years`, `Performance_Category`,
  `Overtime_Category`) are auto-computed if missing from your CSV.
- All charts read from the same filtered dataframe, so every filter in the
  sidebar updates every chart on the active page.
- The visual system (colors, fonts, spacing) lives in `assets/style.css` and
  `config.py` — change tokens there to re-theme the whole app.
