"""
page_modules/ai_insights.py
The "AI Executive Insights" page: sends current KPIs and department summary
to Gemini, renders the generated report, and offers PDF/Markdown/Text
downloads.
"""

import io
import streamlit as st
from config import COL
from utils.data_loader import kpi_summary
import ai


def _filters_description(selections: dict) -> str:
    parts = []
    for key, label in [("department", "Department"), ("gender", "Gender"),
                        ("education", "Education"), ("job_title", "Job Title"),
                        ("performance_category", "Performance Category"),
                        ("remote_freq", "Remote Frequency")]:
        vals = selections.get(key)
        if vals:
            parts.append(f"{label}: {', '.join(map(str, vals))}")
    return "; ".join(parts)


def _report_to_pdf_bytes(report_text: str) -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import simpleSplit

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 2 * cm
    y = height - margin
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "AI Executive Insights Report")
    y -= 1 * cm
    c.setFont("Helvetica", 10)

    for line in report_text.split("\n"):
        wrapped = simpleSplit(line, "Helvetica", 10, width - 2 * margin) or [""]
        for w_line in wrapped:
            if y < margin:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - margin
            c.drawString(margin, y, w_line)
            y -= 0.5 * cm

    c.save()
    buffer.seek(0)
    return buffer.read()


def render(df, selections):
    st.markdown('<div class="page-title">🤖 AI Executive Insights</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Gemini-generated executive analysis, grounded in the current filtered view.</div>',
        unsafe_allow_html=True)

    if df.empty:
        st.markdown('<div class="empty-state"><div class="icon">📭</div>No data available to analyze.</div>',
                    unsafe_allow_html=True)
        return

    kpis = kpi_summary(df)
    filters_desc = _filters_description(selections)
    dept_summary = ai.build_department_summary(df, COL)

    with st.expander("View data being sent to the AI model"):
        st.json(kpis)
        st.text(dept_summary)

    if st.button("🚀 Generate AI Report", use_container_width=True, type="primary"):
        with st.spinner("Analyzing workforce data with Gemini..."):
            report = ai.generate_report(kpis, dept_summary, filters_desc)
            st.session_state["ai_report"] = report

    report = st.session_state.get("ai_report")

    if report:
        st.markdown('<div class="ai-report-card">', unsafe_allow_html=True)
        st.markdown(report)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">EXPORT REPORT</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("⬇ Download as Markdown", report, "ai_executive_report.md",
                                "text/markdown", use_container_width=True)
        with c2:
            st.download_button("⬇ Download as Text", report, "ai_executive_report.txt",
                                "text/plain", use_container_width=True)
        with c3:
            try:
                pdf_bytes = _report_to_pdf_bytes(report)
                st.download_button("⬇ Download as PDF", pdf_bytes, "ai_executive_report.pdf",
                                    "application/pdf", use_container_width=True)
            except ImportError:
                st.caption("Install `reportlab` to enable PDF export.")
    else:
        st.markdown(
            '<div class="empty-state"><div class="icon">🤖</div>'
            'No report generated yet. Click "Generate AI Report" to get an '
            'executive summary, insights, risks, and recommendations based on the current view.</div>',
            unsafe_allow_html=True)
