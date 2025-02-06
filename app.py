"""The main streamlit app that invoke other pages."""
import streamlit as st
from classes.icons import AppIcons
from lib import utils
from lib.datasource import test_connect_to_sheet
from classes.structure import DataStructure 

st.set_page_config(page_title="GTOME", page_icon=AppIcons.MAIN_APP,layout="centered")

st.markdown(utils.hide_streamlit_header(), unsafe_allow_html=True)

if 'language' not in st.session_state or st.session_state.language =="":
    st.session_state.language = "en"

view_page = st.Page("views/dashboard.py", title="Dashboard", icon=AppIcons.DASHBOARD_PAGE)
login_page = st.Page("views/login.py", title="Login", icon=AppIcons.LOG_IN)
error_page = st.Page("views/error.py",title="Error",icon=AppIcons.BUG_REPORT_PAGE)

if st.experimental_user.is_logged_in:
    gsheet_cnn, gsheet_err = test_connect_to_sheet()
    if gsheet_cnn is False:
        error = DataStructure.get_error_object(gsheet_cnn,gsheet_err)
        st.session_state.connection_error = error
        pg = st.navigation([error_page],position="hidden")
    else:
        pg = st.navigation([view_page],position="hidden")
        
else:
        pg = st.navigation([login_page],position="hidden")
pg.run()


