import os
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
import streamlit as st

st.set_page_config(page_title="DataFlow", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

from modules.design import apply_theme
from modules import auth_ui
from modules.home import render_home
from modules.work import render_projects, render_datasets, render_explorer, render_ai, render_settings

apply_theme()

if "page" not in st.session_state:
    st.session_state.page = "landing"

page = st.session_state.page

if page == "landing":
    auth_ui.render_landing()
elif page == "login":
    auth_ui.render_login()
elif page == "register":
    auth_ui.render_register()
elif page == "verify":
    auth_ui.render_verify()
elif page == "recover":
    auth_ui.render_recover()
elif page == "reset":
    auth_ui.render_reset()
elif page == "twofa":
    auth_ui.render_twofa()
elif page == "role":
    auth_ui.render_role()
elif page == "home":
    render_home()
elif page == "projects":
    render_projects()
elif page == "datasets":
    render_datasets()
elif page == "explorer":
    render_explorer()
elif page == "ai":
    render_ai()
elif page == "settings":
    render_settings()
else:
    auth_ui.render_landing()
