import streamlit as st
import plotly.graph_objects as go
from graphics.theme import EMERALD, CARD_BG

def paid_vs_total_gauge(revenue: float, outstanding: float, title="Paid vs Total"):
    percent_paid = 0 if revenue == 0 else max(0, min(1, 1 - (outstanding / revenue)))
    value = round(percent_paid * 100, 1)

    st.markdown(f"<div class='card'><div class='card-header'>📊 {title}</div>", unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'suffix':'%','font':{'size':28}},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': EMERALD},
            'steps': [
                {'range': [0, 50], 'color': '#1a1f1c'},
                {'range': [50, 80], 'color': '#25352e'},
                {'range': [80, 100], 'color': '#325c49'},
            ]
        }
    ))
    fig.update_layout(height=190, margin=dict(l=0,r=0,t=0,b=0),
                      paper_bgcolor=CARD_BG, font={'color':'white'})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
