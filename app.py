"""The main streamlit app that invoke other pages."""
import streamlit as st
from classes import messages
from classes.icons import AppIcons
from lib.datasource import set_user_sheet, test_supabase_connection


if 'user_info' not in st.session_state:
    st.session_state.login = False

if 'language' not in st.session_state or st.session_state.language =="":
    st.session_state.language = "en"

st.set_page_config(page_title="GTOME", page_icon=AppIcons.MAIN_APP,layout="wide")
home_page = st.Page("views/home.py", title="Home", icon=AppIcons.HOME_PAGE)
view_page = st.Page("views/dashboard.py", title="Dashboard", icon=AppIcons.DASHBOARD_PAGE)
login_page = st.Page("views/login.py", title="Login", icon=AppIcons.LOG_IN)
error_page = st.Page("views/error.py",title="Error",icon=AppIcons.BUG_REPORT_PAGE,url_path="/error")
authenticated_pages = [home_page,view_page]

st.session_state.login_query=st.query_params.to_dict()
st.query_params.clear()
try:
    test_supabase_connection()
    if st.session_state.login is True:
        st.session_state.sheet_name = set_user_sheet(st.session_state.user_info['email'])
        pg = st.navigation(authenticated_pages,position="hidden")
    else:
        pg = st.navigation([login_page],position="hidden")
    pg.run()
except ConnectionError:
    pg = st.navigation([error_page],position="hidden")
    pg.run()

