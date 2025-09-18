import streamlit as st
import plotly.express as px
from graphics.data_loader import get_charts_data
from graphics.theme import EMERALD, GOLD, WHITE, CARD_BG

# --- Job Revenue (Top 10) ---
def revenue_bar_top10(invoices, jobs, customers, estimates):
    st.markdown("<div class='card'><div class='card-header'>💼 Job Revenue (Top 10)</div>", unsafe_allow_html=True)
    df = get_charts_data(invoices, jobs, customers, estimates, chart="revenue_by_job")
    if df.empty:
        st.info("No job revenue data available.")
    else:
        df = df.head(10)
        fig = px.bar(
            df, x="job", y="revenue", text_auto=".2s",
            color_discrete_sequence=[EMERALD], template="plotly_dark"
        )
        fig.update_traces(marker_line_color=GOLD, marker_line_width=1)
        fig.update_xaxes(tickangle=-20)
        fig.update_layout(
            height=190, margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            font=dict(color=WHITE), showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# --- Revenue by Source (Donut) ---
def revenue_by_source_donut(invoices, jobs, customers, estimates):
    st.markdown("<div class='card'><div class='card-header'>🧭 Revenue by Source</div>", unsafe_allow_html=True)
    df = get_charts_data(invoices, jobs, customers, estimates, chart="revenue_by_source")
    if df.empty:
        st.info("No revenue by source data available.")
    else:
        fig = px.pie(
            df, names="source", values="revenue",
            color_discrete_sequence=[EMERALD, GOLD, WHITE], template="plotly_dark",
            hole=0.45
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(
            height=190, margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            font=dict(color=WHITE), showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# --- Revenue Trend (Sparkline Line Chart) ---
def revenue_sparkline(invoices, jobs, customers, estimates, title="📈 Revenue Trend"):
    st.markdown(f"<div class='card'><div class='card-header'>{title}</div>", unsafe_allow_html=True)
    df = get_charts_data(invoices, jobs, customers, estimates, chart="revenue_trend")
    if df.empty:
        st.info("No revenue trend data available.")
    else:
        fig = px.line(
            df, x="date", y="revenue", markers=True,
            color_discrete_sequence=[GOLD], template="plotly_dark"
        )
        fig.update_traces(line=dict(width=2), marker=dict(size=6, color=EMERALD))
        fig.update_layout(
            height=190, margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            font=dict(color=WHITE)
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
