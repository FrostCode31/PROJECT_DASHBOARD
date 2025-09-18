import streamlit as st
import plotly.express as px
import pandas as pd
from graphics.theme import EMERALD, GOLD, WHITE, CARD_BG

def top_customers_chart(invoices):
    st.markdown("<div class='card'><div class='card-header'>👑 Top Customers by Revenue</div>", unsafe_allow_html=True)
    df = pd.DataFrame(invoices)
    if df.empty or "customer.name" not in df:
        st.info("No customer revenue data available.")
    else:
        if "amount" in df:
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
        top_cust = df.groupby("customer.name")["amount"].sum().reset_index().sort_values("amount", ascending=False).head(5)
        fig = px.bar(top_cust, x="customer.name", y="amount", text_auto=".2s",
                     color_discrete_sequence=[EMERALD], template="plotly_dark")
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, height=240)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def outstanding_by_customer_chart(invoices):
    st.markdown("<div class='card'><div class='card-header'>💸 Outstanding by Customer</div>", unsafe_allow_html=True)
    df = pd.DataFrame(invoices)
    if df.empty or "customer.name" not in df or "due_amount" not in df:
        st.info("No outstanding balance data available.")
    else:
        df["due_amount"] = pd.to_numeric(df["due_amount"], errors="coerce").fillna(0)
        top_due = df.groupby("customer.name")["due_amount"].sum().reset_index().sort_values("due_amount", ascending=False).head(5)
        fig = px.bar(top_due, x="customer.name", y="due_amount", text_auto=".2s",
                     color_discrete_sequence=[GOLD], template="plotly_dark")
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, height=240)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def monthly_jobs_trend(jobs):
    st.markdown("<div class='card'><div class='card-header'>📅 Monthly Jobs Trend</div>", unsafe_allow_html=True)
    df = pd.DataFrame(jobs)
    if df.empty or "created_at" not in df:
        st.info("No job trend data available.")
    else:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        trend = df.groupby(df["created_at"].dt.to_period("M")).size().reset_index(name="jobs")
        trend["created_at"] = trend["created_at"].astype(str)
        fig = px.line(trend, x="created_at", y="jobs", markers=True,
                      color_discrete_sequence=[EMERALD], template="plotly_dark")
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, height=240)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def conversion_funnel(jobs, invoices, customers):
    st.markdown("<div class='card'><div class='card-header'>🔀 Conversion Funnel</div>", unsafe_allow_html=True)
    leads = len(customers)
    booked = len(jobs)
    invoices_count = len(invoices)
    df = pd.DataFrame({
        "Stage": ["Leads", "Jobs Booked", "Invoices"],
        "Count": [leads, booked, invoices_count]
    })
    fig = px.funnel(df, x="Count", y="Stage", color_discrete_sequence=[EMERALD, GOLD, WHITE], template="plotly_dark")
    fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, height=240)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
