import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from graphics.theme import CARD_BG, EMERALD, GOLD, WHITE

def geo_map(data):
    rows = []
    for rec in data:
        if "addresses" in rec:
            for addr in rec.get("addresses", []):
                country = (addr.get("country") or "").upper()
                if country in ["US", "USA", "UNITED STATES", "UNITED STATES OF AMERICA", "U.S."]:
                    rows.append("United States")

    if not rows:
        st.info("No US data available.")
        return

    df = pd.Series(rows).value_counts().reset_index()
    df.columns = ["Country", "Count"]

    # Base globe (transparent background)
    fig = go.Figure(
        data=go.Choropleth(
            locations=df["Country"],
            z=df["Count"],
            locationmode="country names",
            colorscale=[[0, EMERALD], [0.5, GOLD], [1, WHITE]],
            marker_line_color="gray",
            colorbar_title="Count",
            hoverlabel=dict(
                bgcolor="black",
                font_color=EMERALD,
                font_size=14,
                font_family="Inter"
            )
        )
    )

    # Rotation frames (auto-rotation)
    frames = []
    for lon in range(-180, 181, 2):
        frames.append(go.Frame(
            layout=dict(
                geo=dict(projection_rotation=dict(lon=lon, lat=30, roll=0))
            )
        ))
    fig.frames = frames

    # Layout → transparent globe with rotation
    fig.update_layout(
        geo=dict(
            projection_type="orthographic",
            showland=True,
            landcolor=EMERALD,
            showocean=False,
            showcountries=True,
            countrycolor="gray",
            projection_rotation=dict(lon=-95, lat=30, roll=0),
            bgcolor="rgba(0,0,0,0)"  # 🔑 fully transparent
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=500,
        dragmode="orbit",
        sliders=[{"steps": []}],
        updatemenus=[{
            "type": "buttons",
            "buttons": [
                {
                    "label": "",
                    "method": "animate",
                    "args": [None, {
                        "frame": {"duration": 120, "redraw": True},
                        "fromcurrent": True,
                        "mode": "immediate",
                        "transition": {"duration": 0},
                        "repeat": True
                    }]
                }
            ]
        }]
    )

    # CSS Glow + Pulse (aligned to globe)
    st.markdown(
        f"""
        <style>
        .globe-wrapper {{
            position: relative;
            display: flex;
            justify-content: center;
            align-items: bottom;
        }}
        /* Base glow halo */
        .glow-circle {{
            position: absolute;
            width: 520px;
            height: 520px;
            border-radius: 50%;
            background: radial-gradient(circle, {EMERALD}55 0%, transparent 70%);
            filter: blur(60px);
            z-index: 0;
        }}
        /* Expanding pulse */
        .pulse {{
            position: absolute;
            width: 540px;
            height: 540px;
            border-radius: 50%;
            background: radial-gradient(circle, {EMERALD}99 0%, transparent 80%);
            animation: pulseAnim 2s infinite;
            opacity: 0.6;
            z-index: 0;
        }}
        @keyframes pulseAnim {{
            0%   {{ transform: scale(1); opacity: 0.6; }}
            70%  {{ transform: scale(1.3); opacity: 0; }}
            100% {{ transform: scale(1.3); opacity: 0; }}
        }}
        /* Hover glow effect for countries */
        .js-plotly-plot .plotly .choroplethlayer path:hover {{
            stroke: {GOLD} !important;
            stroke-width: 3 !important;
            filter: drop-shadow(0px 0px 8px {GOLD});
        }}
        </style>
        <div class="globe-wrapper">
            <div class="glow-circle"></div>
            <div class="pulse"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.plotly_chart(fig, use_container_width=True)


def geo_section(invoices, jobs, customers, leads):
    st.markdown("<div class='card'><div class='card-header'>🌍 Interactive Globe View</div>", unsafe_allow_html=True)

    option = st.selectbox(
        "Select dataset",
        ["Customers", "Jobs", "Leads", "Invoices"],
        index=0
    )

    if option == "Customers":
        geo_map(customers)
    elif option == "Jobs":
        geo_map(jobs)
    elif option == "Leads":
        geo_map(leads)
    elif option == "Invoices":
        geo_map(invoices)

    st.markdown("</div>", unsafe_allow_html=True)
