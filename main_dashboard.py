import streamlit as st

from graphics.kpi_section import kpi_section
from graphics.finance_charts import revenue_bar_top10, revenue_by_source_donut, revenue_sparkline
from graphics.leads_charts import leads_by_source, leads_sparkline, leads_goal_progress
from graphics.jobs_charts import jobs_by_status
from graphics.geo_charts import geo_section
from graphics.details_charts import details_charts
from graphics.progress_card import paid_vs_total_gauge
from graphics.data_loader import load_data, apply_filters
from graphics.filters import dashboard_filters
from graphics.metrics import get_kpis, get_charts_data

# Utility for section headers
def section_title(title, emoji="📊"):
    st.markdown(
        f"""
        <div style="
            font-size:1.5rem;
            font-weight:1000;
            color:var(--emerald);
            border-bottom:1px solid var(--gold);
            margin:0.6rem 0 0.4rem 0;
            padding-bottom:0.2rem;
        ">
            {emoji} {title}
        </div>
        """,
        unsafe_allow_html=True
    )

def show_main_dashboard():
    # Load + apply filters
    invoices, jobs, customers, estimates = load_data()
    filter_values = dashboard_filters()
    invoices, jobs, customers, estimates = apply_filters(
        invoices, jobs, customers, estimates, filter_values
    )

    # -----------------------------
    # 0. Compute KPIs first
    # -----------------------------
    kpis = get_kpis(invoices, jobs, customers, estimates)

    # -----------------------------
    # 1. KPI Row
    # -----------------------------
    section_title("Key Performance Indicators", "📌")
    #  Pass only 1 positional (kpis) and the rest as keyword args
    #  Do NOT pass estimates here (kpi_section doesn't take it)
    kpi_section(
        kpis,
        invoices=invoices,
        jobs=jobs,
        customers=customers,
        get_charts_data=get_charts_data,
    )

    # -----------------------------
    # 2. Globe centerpiece
    # -----------------------------
    section_title("Geographic Insights", "🌍")
    geo_section(invoices, jobs, customers, estimates)

    # -----------------------------
    # 3. Trends
    # -----------------------------
    section_title("Trends & Growth", "📈")
    col1, col2 = st.columns(2, gap="small")
    with col1:
        revenue_sparkline(invoices, jobs, customers, estimates, title="📈 Revenue Trend (MoM)")
    with col2:
        leads_sparkline(invoices, jobs, customers, estimates, title="📈 Leads Trend (MoM)")

    # -----------------------------
    # 4. Revenue Breakdown
    # -----------------------------
    section_title("Revenue Breakdown", "💰")
    col3, col4 = st.columns(2, gap="small")
    with col3:
        revenue_bar_top10(invoices, jobs, customers, estimates)
    with col4:
        revenue_by_source_donut(invoices, jobs, customers, estimates)

    # -----------------------------
    # 5. Jobs & Leads Overview
    # -----------------------------
    section_title("Jobs & Leads Overview", "🧾")
    col5, col6 = st.columns(2, gap="small")
    with col5:
        jobs_by_status(invoices, jobs, customers, estimates)
    with col6:
        leads_by_source(invoices, jobs, customers, estimates)

    # -----------------------------
    # 6. Financial Health
    # -----------------------------
    section_title("Financial Health", "💹")
    paid_vs_total_gauge(
        revenue=sum(i.get("amount", 0) for i in invoices),
        outstanding=sum(i.get("due_amount", 0) for i in invoices)
    )

    # -----------------------------
    # 7. Detailed Records
    # -----------------------------
    section_title("Detailed Records", "📑")
    details_charts(invoices, jobs)
