import streamlit as st
from datetime import date, timedelta
from graphics.data_loader import load_data, get_unique_options

def dashboard_filters():
    # Sidebar title
    st.sidebar.markdown(
        "<div style='font-size:18px;font-weight:700;color:#e8efe9;margin-bottom:6px;'>Filters</div>",
        unsafe_allow_html=True
    )

    today = date.today()
    col_a, col_b = st.sidebar.columns(2)
    date_from = col_a.date_input("From", today - timedelta(days=90), label_visibility="collapsed")
    date_to   = col_b.date_input("To", today, label_visibility="collapsed")

    st.sidebar.markdown(
        "<div style='color:#9fb0ad;font-size:12px;margin-top:-10px;margin-bottom:8px;'>Date Range</div>",
        unsafe_allow_html=True
    )

    # Search box
    search = st.sidebar.text_input("🔎 Search", placeholder="Any field...")

    # Auto-populate options from current data
    _, jobs, customers, _ = load_data()
    job_statuses_opts, lead_sources_opts = get_unique_options(jobs, customers)

    lead_sources = st.sidebar.multiselect(
        "Lead Sources", options=lead_sources_opts, default=[],
        placeholder="Select sources..."
    )
    job_statuses = st.sidebar.multiselect(
        "Job Statuses", options=job_statuses_opts, default=[],
        placeholder="Select statuses..."
    )

    # Toggle for live interaction
    st.sidebar.markdown("---")
    live = st.sidebar.toggle("Enable Live Interactions", True)

    return {
        "date_from": date_from,
        "date_to": date_to,
        "search": search,
        "lead_sources": lead_sources,
        "job_statuses": job_statuses,
        "live": live,
    }
