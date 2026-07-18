"""
charts.py
Every Plotly chart-builder function used across the dashboard lives here so
pages stay thin and charts stay consistent. Each function takes a (filtered)
dataframe and returns a ready-to-render go.Figure.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from config import COL, COLORS


def _empty_fig(message="No data available for the current filters"):
    fig = go.Figure()
    fig.add_annotation(text=message, showarrow=False, font=dict(size=14, color=COLORS["text_muted"]))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(height=320)
    return fig


def _guard(df, cols):
    if df.empty or any(c not in df.columns for c in cols):
        return False
    return True


# ---------------------------------------------------------------- distributions
def department_distribution(df):
    if not _guard(df, [COL["department"]]):
        return _empty_fig()
    counts = df[COL["department"]].value_counts().reset_index()
    counts.columns = ["Department", "Count"]
    fig = px.bar(counts, x="Count", y="Department", orientation="h",
                 title="Department Distribution", text="Count")
    fig.update_traces(marker_color=COLORS["accent"], textposition="outside")
    fig.update_layout(yaxis=dict(categoryorder="total ascending"), height=380)
    return fig


def gender_distribution(df):
    if not _guard(df, [COL["gender"]]):
        return _empty_fig()
    counts = df[COL["gender"]].value_counts().reset_index()
    counts.columns = ["Gender", "Count"]
    fig = px.pie(counts, names="Gender", values="Count", hole=0.55, title="Gender Distribution")
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(height=360)
    return fig


def education_distribution(df):
    if not _guard(df, [COL["education"]]):
        return _empty_fig()
    counts = df[COL["education"]].value_counts().reset_index()
    counts.columns = ["Education", "Count"]
    fig = px.bar(counts, x="Education", y="Count", title="Education Distribution", text="Count")
    fig.update_traces(marker_color=COLORS["accent_alt"], textposition="outside")
    fig.update_layout(height=360)
    return fig


def performance_distribution(df):
    if not _guard(df, [COL["performance"]]):
        return _empty_fig()
    fig = px.histogram(df, x=COL["performance"], nbins=25, title="Performance Score Distribution")
    fig.update_traces(marker_color=COLORS["accent"])
    fig.update_layout(height=360, bargap=0.05)
    return fig


def performance_category_distribution(df):
    if not _guard(df, [COL["performance_category"]]):
        return _empty_fig()
    order = ["Excellent", "Good", "Average", "Needs Improvement"]
    counts = df[COL["performance_category"]].value_counts().reindex(order).dropna().reset_index()
    counts.columns = ["Category", "Count"]
    fig = px.bar(counts, x="Category", y="Count", title="Performance Category Distribution",
                 text="Count", color="Category",
                 color_discrete_sequence=COLORS["chart_sequence"])
    fig.update_traces(textposition="outside")
    fig.update_layout(height=360, showlegend=False)
    return fig


def salary_distribution(df):
    if not _guard(df, [COL["salary"]]):
        return _empty_fig()
    fig = px.histogram(df, x=COL["salary"], nbins=30, title="Salary Distribution")
    fig.update_traces(marker_color=COLORS["accent_alt"])
    fig.update_layout(height=360, bargap=0.05)
    return fig


def satisfaction_distribution(df):
    if not _guard(df, [COL["satisfaction"]]):
        return _empty_fig()
    fig = px.histogram(df, x=COL["satisfaction"], nbins=20, title="Satisfaction Score Distribution")
    fig.update_traces(marker_color=COLORS["success"])
    fig.update_layout(height=360, bargap=0.05)
    return fig


# ---------------------------------------------------------------- by-department
def avg_performance_by_department(df):
    if not _guard(df, [COL["department"], COL["performance"]]):
        return _empty_fig()
    agg = df.groupby(COL["department"])[COL["performance"]].mean().sort_values().reset_index()
    fig = px.bar(agg, x=COL["performance"], y=COL["department"], orientation="h",
                 title="Average Performance by Department", text_auto=".2f")
    fig.update_traces(marker_color=COLORS["accent"])
    fig.update_layout(height=400)
    return fig


def avg_salary_by_department(df):
    if not _guard(df, [COL["department"], COL["salary"]]):
        return _empty_fig()
    agg = df.groupby(COL["department"])[COL["salary"]].mean().sort_values().reset_index()
    fig = px.bar(agg, x=COL["salary"], y=COL["department"], orientation="h",
                 title="Average Salary by Department", text_auto=".2s")
    fig.update_traces(marker_color=COLORS["accent_alt"])
    fig.update_layout(height=400)
    return fig


def job_title_performance(df):
    if not _guard(df, [COL["job_title"], COL["performance"]]):
        return _empty_fig()
    agg = (df.groupby(COL["job_title"])[COL["performance"]].mean()
           .sort_values(ascending=False).head(15).reset_index())
    fig = px.bar(agg, x=COL["performance"], y=COL["job_title"], orientation="h",
                 title="Performance by Job Title (Top 15)", text_auto=".2f")
    fig.update_traces(marker_color=COLORS["warning"])
    fig.update_layout(yaxis=dict(categoryorder="total ascending"), height=460)
    return fig


# ---------------------------------------------------------------- relationships
def scatter_relationship(df, x_col, y_col, title, color_col=None):
    if not _guard(df, [x_col, y_col]):
        return _empty_fig()
    fig = px.scatter(df, x=x_col, y=y_col, title=title, opacity=0.55,
                      color=color_col if color_col and color_col in df.columns else None,
                      color_discrete_sequence=COLORS["chart_sequence"],
                      trendline="ols")
    fig.update_layout(height=400)
    return fig


def training_vs_performance(df):
    return scatter_relationship(df, COL["training_hours"], COL["performance"],
                                 "Training Hours vs Performance")


def salary_vs_performance(df):
    return scatter_relationship(df, COL["performance"], COL["salary"],
                                 "Salary vs Performance")


def satisfaction_vs_performance(df):
    return scatter_relationship(df, COL["satisfaction"], COL["performance"],
                                 "Satisfaction vs Performance")


def projects_vs_performance(df):
    return scatter_relationship(df, COL["projects"], COL["performance"],
                                 "Projects Handled vs Performance")


def years_vs_performance(df):
    return scatter_relationship(df, COL["years_at_company"], COL["performance"],
                                 "Years at Company vs Performance")


def overtime_vs_performance(df):
    return scatter_relationship(df, COL["overtime"], COL["performance"],
                                 "Overtime Hours vs Performance")


# ---------------------------------------------------------------- remote work / promotions
def remote_work_analysis(df):
    if not _guard(df, [COL["remote_freq"], COL["performance"]]):
        return _empty_fig()
    agg = df.groupby(COL["remote_freq"])[COL["performance"]].mean().reset_index()
    agg = agg.sort_values(COL["remote_freq"])
    fig = px.bar(agg, x=COL["remote_freq"], y=COL["performance"],
                 title="Average Performance by Remote Work Frequency (%)", text_auto=".2f")
    fig.update_traces(marker_color=COLORS["accent"])
    fig.update_layout(height=380)
    return fig


def promotion_analysis(df):
    if not _guard(df, [COL["promotions"], COL["performance"]]):
        return _empty_fig()
    agg = df.groupby(COL["promotions"])[COL["performance"]].mean().reset_index()
    fig = px.bar(agg, x=COL["promotions"], y=COL["performance"],
                 title="Average Performance by Number of Promotions", text_auto=".2f")
    fig.update_traces(marker_color=COLORS["accent_alt"])
    fig.update_layout(height=380)
    return fig


# ---------------------------------------------------------------- correlation
def correlation_heatmap(df):
    numeric_cols = [c for c in [
        COL["age"], COL["years_at_company"], COL["performance"], COL["salary"],
        COL["work_hours"], COL["projects"], COL["overtime"], COL["sick_days"],
        COL["team_size"], COL["training_hours"], COL["promotions"], COL["satisfaction"],
    ] if c in df.columns]
    if df.empty or len(numeric_cols) < 2:
        return _empty_fig()
    corr = df[numeric_cols].corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale=
                     [[0, COLORS["danger"]], [0.5, COLORS["bg_card"]], [1, COLORS["accent"]]],
                     title="Correlation Matrix", aspect="auto")
    fig.update_layout(height=560)
    return fig


# ---------------------------------------------------------------- rankings
def top_bottom_employees(df, n=10, top=True):
    if not _guard(df, [COL["id"], COL["performance"]]):
        return pd.DataFrame()
    sorted_df = df.sort_values(COL["performance"], ascending=not top)
    cols = [c for c in [COL["id"], COL["department"], COL["job_title"],
                        COL["performance"], COL["salary"], COL["satisfaction"]] if c in df.columns]
    return sorted_df[cols].head(n).reset_index(drop=True)
