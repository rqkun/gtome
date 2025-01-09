"""The main streamlit app that invoke other pages."""
import streamlit as st
from classes import messages
from classes.icons import AppIcons
from lib.datasource import set_user_sheet, test_connect_to_sheet, test_supabase_connection
from classes.structure import DataStructure 

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
    supbase_cnn, supbase_err = test_supabase_connection()
    gsheet_cnn, gsheet_err = test_connect_to_sheet()
    if (supbase_cnn is False or gsheet_cnn is False):
        raise ConnectionError()
    if st.session_state.login is True:
        st.session_state.sheet_name = set_user_sheet(st.session_state.user_info['email'])
        pg = st.navigation(authenticated_pages,position="hidden")
    else:
        pg = st.navigation([login_page],position="hidden")
    pg.run()
except ConnectionError:
    error = DataStructure.get_error_object(supbase_cnn,gsheet_cnn,supbase_err,gsheet_err)
    st.session_state.connection_error = error
    pg = st.navigation([error_page],position="hidden")
    pg.run()

