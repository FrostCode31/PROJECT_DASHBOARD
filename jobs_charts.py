import streamlit as st
import plotly.express as px
from graphics.data_loader import get_charts_data
from graphics.theme import EMERALD, CARD_BG

def jobs_by_status(invoices, jobs, customers, estimates):
    st.markdown("<div class='card'><div class='card-header'>🛠️ Jobs by Status</div>", unsafe_allow_html=True)
    df = get_charts_data(invoices, jobs, customers, estimates, chart="jobs_status")
    if df.empty:
        st.info("No job status data available.")
    else:
        fig = px.bar(df, x="status", y="count", text_auto=True,
                     color_discrete_sequence=[EMERALD], template="plotly_dark")
        fig.update_layout(height=190, margin=dict(l=0,r=0,t=0,b=0),
                          paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
