import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go

DATA_FOLDER = "ERROR"

def load_json(filename):
    with open(os.path.join(DATA_FOLDER, filename), encoding="utf-8") as f:
        return json.load(f)

def show_data_info():
    st.markdown("# 👥 Customers")
    st.markdown("<div class='subtitle'>Customer Insights & Details</div>", unsafe_allow_html=True)

    # --- Load datasets ---
    customers = load_json("customers_data.json")
    jobs = load_json("jobs_data.json")
    leads = load_json("estimates_data.json")   # using estimates as leads
    invoices = load_json("invoices_data.json")

    df_customers = pd.json_normalize(customers)
    df_jobs = pd.json_normalize(jobs)
    df_leads = pd.json_normalize(leads)

    if df_customers.empty:
        st.warning("No customer data available.")
        return

    # Ensure datetime conversion
    if "created_at" in df_customers:
        df_customers["created_at"] = pd.to_datetime(df_customers["created_at"], errors="coerce")
    if "updated_at" in df_customers:
        df_customers["updated_at"] = pd.to_datetime(df_customers["updated_at"], errors="coerce")

    # === ROW 1: KPI CARDS ===
    c1, c2, c3, c4 = st.columns(4, gap="small")

    with c1:
        st.markdown(f"""
            <div class='card kpi-card'>
                <div class='card-header'>📊 Total Customers</div>
                <div class='kpi-value'>{len(df_customers):,}</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class='card kpi-card'>
                <div class='card-header'>🧲 Leads</div>
                <div class='kpi-value'>{len(df_leads):,}</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class='card kpi-card'>
                <div class='card-header'>🗂 Jobs</div>
                <div class='kpi-value'>{len(df_jobs):,}</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        recent = df_customers[df_customers["updated_at"] >= (df_customers["updated_at"].max() - pd.Timedelta(days=30))] if "updated_at" in df_customers else []
        st.markdown(f"""
            <div class='card kpi-card'>
                <div class='card-header'>⏱ Updated Last 30d</div>
                <div class='kpi-value'>{len(recent):,}</div>
            </div>
        """, unsafe_allow_html=True)

    # === ROW 2: CHARTS ===
    c5, c6 = st.columns([2,1], gap="small")
    with c5:
        st.markdown("<div class='card'><div class='card-header'>📈 Customer Growth</div>", unsafe_allow_html=True)
        if "created_at" in df_customers:
            trend = df_customers.groupby(df_customers["created_at"].dt.to_period("M")).size().reset_index(name="customers")
            trend["created_at"] = trend["created_at"].astype(str)
            fig = px.line(
                trend, x="created_at", y="customers", markers=True,
                color_discrete_sequence=["#008060"], template="plotly_dark"
            )
            fig.update_layout(
                margin=dict(l=0,r=0,t=0,b=0), height=220,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white")
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c6:
        st.markdown("<div class='card'><div class='card-header'>🧭 Lead Sources</div>", unsafe_allow_html=True)
        if "lead_source" in df_customers:
            pie = df_customers["lead_source"].fillna("Unknown").value_counts().reset_index()
            pie.columns = ["Source","Count"]
            fig2 = px.pie(
                pie, names="Source", values="Count",
                color_discrete_sequence=["#008060","#d4af37","#94a3a1","#0f9d58"],
                template="plotly_dark"
            )
            fig2.update_traces(textposition="inside", textinfo="percent+label")
            fig2.update_layout(
                margin=dict(l=0,r=0,t=0,b=0), height=220,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"), showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # === ROW 3: TABLE + DETAILS ===
    c7, c8 = st.columns([1,1], gap="small")
    with c7:
        st.markdown("<div class='card'><div class='card-header'>🧾 Recent Customers</div>", unsafe_allow_html=True)
        show_cols = [c for c in ["first_name","last_name","email","lead_source","created_at"] if c in df_customers.columns]
        df_recent = df_customers[show_cols].sort_values(by="created_at", ascending=False).head(7)

        # Plotly Table instead of st.dataframe
        fig_table = go.Figure(
            data=[go.Table(
                header=dict(
                    values=[f"<b>{col}</b>" for col in df_recent.columns],
                    fill_color="#008060",  # emerald header
                    font=dict(color="white", size=12),
                    align="left"
                ),
                cells=dict(
                    values=[df_recent[col] for col in df_recent.columns],
                    fill_color=[["#121a17", "#0f1513"] * (len(df_recent)//2 + 1)],  # striped rows
                    font=dict(color="white", size=11),
                    align="left"
                )
            )]
        )
        fig_table.update_layout(
            margin=dict(l=0,r=0,t=0,b=0),
            height=220,
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_table, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c8:
        st.markdown("<div class='card'><div class='card-header'>🧑‍💼 Customer Details</div>", unsafe_allow_html=True)
        names = (df_customers.get("first_name", pd.Series()).fillna("") + " " + df_customers.get("last_name", pd.Series()).fillna("")).tolist()
        selected = st.selectbox("Select Customer", options=names)
        if selected:
            idx = names.index(selected)
            cust = customers[idx]
            for key, value in cust.items():
                st.markdown(f"<span style='color:#d4af37;font-weight:600'>{key}</span>: <span style='color:white'>{value}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
