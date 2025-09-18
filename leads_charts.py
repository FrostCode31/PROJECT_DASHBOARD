import streamlit as st
import plotly.express as px
import pandas as pd
from graphics.data_loader import get_charts_data
from graphics.theme import EMERALD, GOLD, WHITE, CARD_BG

def leads_by_source(invoices, jobs, customers, estimates):
    st.markdown("<div class='card'><div class='card-header'>🧲 Leads by Source</div>", unsafe_allow_html=True)
    df = get_charts_data(invoices, jobs, customers, estimates, chart="leads_by_source")
    if df.empty:
        st.info("No lead source data available.")
    else:
        fig = px.bar(df.sort_values("count", ascending=False), x="source", y="count",
                     text_auto=True, color_discrete_sequence=[EMERALD], template="plotly_dark")
        fig.update_layout(height=190, margin=dict(l=0,r=0,t=0,b=0),
                          paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def leads_sparkline(invoices, jobs, customers, estimates, title="📈 Leads Trend"):
    st.markdown(f"<div class='card'><div class='card-header'>{title}</div>", unsafe_allow_html=True)
    df = get_charts_data(invoices, jobs, customers, estimates, chart="leads_trend")
    if df.empty:
        st.info("No leads trend data available.")
    else:
        fig = px.line(df, x="date", y="leads", markers=True,
                      color_discrete_sequence=[GOLD], template="plotly_dark")
        fig.update_layout(height=190, margin=dict(l=0,r=0,t=0,b=0),
                          paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def leads_goal_progress(customers, monthly_goal: int = None):
    import pandas as pd
    st.markdown("<div class='card'><div class='card-header'>🎯 Leads (This Month)</div>", unsafe_allow_html=True)
    df = pd.DataFrame(customers)
    curr = 0
    if not df.empty and "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce").dt.tz_localize(None)
        today = pd.Timestamp.today().tz_localize(None)
        this_month = (df["created_at"].dt.year == today.year) & (df["created_at"].dt.month == today.month)
        curr = int(this_month.sum())
    goal = monthly_goal or max(50, int(curr * 1.2) + 5)
    pct = 0 if goal == 0 else min(100, round(100 * curr / goal, 1))

    st.markdown(f"""
        <div style="color:#eaeff0;font-weight:800;font-size:1.3rem;margin:2px 0 4px 2px;">{curr:,}</div>
        <div class="progress-wrap"><div class="progress-bar" style="width:{pct}%"></div></div>
        <div style="color:#9fb0ad;margin-top:4px;font-size:0.8rem;">Goal: {goal:,} &nbsp;•&nbsp; {pct}%</div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
