import streamlit as st

# Palette (greens)
EMERALD = "#008060"      # brand emerald
GOLD    = "#d4af37"
WHITE   = "#ffffff"
DARK_BG = "#0b0f0d"      # near-black with green tint
CARD_BG = "#121a17"      # deep greenish charcoal
MUTED   = "#9fb0ad"      # desaturated green-gray
INK     = "#e8efe9"      # light ink for numbers

def inject_theme():
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

            html, body, [class*="css"] {{
                font-family: 'Inter', sans-serif !important;
            }}

            :root {{
                --emerald: {EMERALD};
                --gold: {GOLD};
                --white: {WHITE};
                --dark: {DARK_BG};
                --card: {CARD_BG};
                --muted: {MUTED};
                --ink:   {INK};
            }}

            html, body, .main, .block-container {{ background: var(--dark) !important; }}
            .block-container {{ max-width: 1500px !important; padding: .4rem .6rem .6rem .6rem !important; }}
            header, footer, [data-testid="stStatusWidget"] {{ display:none !important; }}

            /* --- PAGE TITLE BAR --- */
            [data-testid="stHeader"] {{
                background: var(--dark) !important;
                display: flex;
                justify-content: center !important;
                align-items: center !important;
                padding: 0.6rem 0 !important;
                border-bottom: 1px solid var(--gold);
            }}
            [data-testid="stHeader"] .stAppHeader {{ display: none !important; }}

            .app-title {{
                font-size: 28px;
                font-weight: 900;
                color: var(--emerald);
                text-align: center;
                letter-spacing: 1px;
                text-shadow: 0px 0px 8px rgba(0, 128, 96, 0.5);
            }}
            .app-subtitle {{
                font-size: 14px;
                font-weight: 500;
                color: var(--muted);
                text-align: center;
                margin-top: 2px;
            }}

            /* --- Tabs --- */
            .stTabs [data-baseweb="tab"] {{
                background: var(--card) !important;
                color: var(--muted) !important;
                border: 1px solid var(--gold) !important;
                border-bottom: none !important;
                font-weight: 600;
                font-size: 0.95rem;
                margin-right: 6px;
                border-radius: 6px 6px 0 0;
                transition: all 0.25s ease-in-out;
                padding: 0.4rem 0.9rem !important;
            }}
            .stTabs [data-baseweb="tab"]:hover {{
                box-shadow: 0 0 8px var(--emerald);
                color: var(--white) !important;
            }}
            .stTabs [aria-selected="true"] {{
                background: var(--emerald) !important;
                color: var(--white) !important;
                border: 1px solid var(--gold) !important;
                border-bottom: none !important;
                font-weight: 700;
                box-shadow: 0 0 12px rgba(0,128,96,0.6);
            }}

            /* --- Card containers --- */
            .card {{
                background: var(--card) !important;
                border: 1px solid var(--gold);
                border-radius: 10px;
                padding: 6px 8px;
                box-shadow: 0 1px 6px rgba(0,0,0,.38);
                margin-bottom: .6rem;
                transition: all 0.25s ease-in-out;
            }}
            .card:hover {{
                box-shadow: 0 0 14px var(--emerald);
                transform: translateY(-2px);
            }}
            .card-header {{
                display:flex; align-items:center; gap:.5rem;
                color: var(--emerald) !important;
                font-weight: 700;
                font-size: 0.9rem;
                margin: 2px 4px 6px 4px;
            }}

            /* --- KPI tiles --- */
            .kpi {{
                background: var(--card) !important;
                border: 1px solid var(--gold);
                border-radius: 10px;
                padding: 10px 14px;
                display:flex; flex-direction:column; gap:2px;
                min-height: 60px;
                box-shadow: 0 2px 10px rgba(0,0,0,.35);
                transition: all 0.25s ease-in-out;
            }}
            .kpi:hover {{
                box-shadow: 0 0 14px var(--emerald);
                transform: translateY(-2px);
            }}
            .kpi .kpi-title {{ color: var(--emerald); font-weight:700; font-size: .9rem; }}
            .kpi .kpi-value {{ color: var(--white); font-weight:900; font-size: 1.6rem; line-height:1; }}

            /* --- DataFrames & Tables --- */
            .stDataFrame, .stTable {{
                background: var(--card) !important;
                border: 1px solid var(--gold) !important;
                border-radius: 6px;
                color: var(--white) !important;
            }}
            .stDataFrame td, .stDataFrame th,
            .stTable td, .stTable th {{
                background: var(--card) !important;
                color: var(--white) !important;
                border-color: var(--gold) !important;
            }}

            /* --- Dropdown (Selectbox) --- */
            div[data-baseweb="select"] > div {{
                background-color: var(--card) !important;
                border: 1px solid var(--gold) !important;
                color: var(--white) !important;
                font-weight: 600 !important;
                border-radius: 8px !important;
                transition: all 0.25s ease-in-out;
            }}
            div[data-baseweb="select"] > div:hover {{
                box-shadow: 0 0 10px var(--emerald);
                transform: translateY(-1px);
            }}
            div[data-baseweb="select"] svg {{
                fill: var(--gold) !important;
            }}

            /* --- Sidebar --- */
            section[data-testid="stSidebar"] {{
                background-color: var(--card) !important;
                border-right: 1px solid var(--gold);
                padding-top: 0.8rem !important;
            }}
            section[data-testid="stSidebar"] .stMarkdown,
            section[data-testid="stSidebar"] label {{
                color: var(--white) !important;
                font-weight: 600 !important;
                font-size: 0.9rem !important;
            }}
            section[data-testid="stSidebar"] .stTextInput input,
            section[data-testid="stSidebar"] .stDateInput input,
            section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {{
                background-color: #0f1513 !important;
                color: var(--white) !important;
                border: 1px solid var(--gold) !important;
                border-radius: 6px !important;
                font-size: 0.88rem !important;
                padding: 4px 8px !important;
            }}
            section[data-testid="stSidebar"] input::placeholder {{
                color: var(--muted) !important;
            }}

            /* --- Toggle --- */
            section[data-testid="stSidebar"] [data-testid="stWidgetCheckbox"] div[role="checkbox"] {{
                border: 1px solid var(--gold) !important;
                background-color: #0f1513 !important;
            }}
            section[data-testid="stSidebar"] [data-testid="stWidgetCheckbox"][aria-checked="true"] div[role="checkbox"] {{
                background-color: var(--emerald) !important;
            }}

            /* --- Multiselect chips --- */
            section[data-testid="stSidebar"] [data-baseweb="tag"] {{
                background-color: var(--emerald) !important;
                color: var(--white) !important;
                font-weight: 600;
                border-radius: 4px !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
