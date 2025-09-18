import streamlit as st
from graphics.main_dashboard import show_main_dashboard
from pages.data_info import show_data_info
from pages.update_download import show_update_download
from graphics.theme import inject_theme

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Lead to Revenue Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply global theme
inject_theme()

# ----------------------------
# HEADER (Custom Title)
# ----------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top:-35px; margin-bottom:20px;">
        <div class="app-title">LEAD TO REVENUE DASHBOARD</div>
        <div class="app-subtitle">IT'S CRAZYYYYY</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# NAVIGATION TABS
# ----------------------------
tabs = st.tabs(["📊 Graphics", "📂 Data Info", "⬇️ Download & History"])

with tabs[0]:
    show_main_dashboard()

with tabs[1]:
    show_data_info()

with tabs[2]:
    show_update_download()
