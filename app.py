"""The main streamlit app that invoke other pages."""
import streamlit as st
from classes.icons import AppIcons
from lib.datasource import get_user_sheet, set_user_sheet, test_supabase_connection


if 'user_info' not in st.session_state:
    st.session_state.login = False

# ms = st.session_state
# if "themes" not in ms:
#     ms.themes = {"current_theme": "dark",
#                     "refreshed": True,
#                     "light": {"theme.base": "dark",
#                               "button_face": ":material/dark_mode:"},

#                     "dark":  {"theme.base": "light",
#                               "button_face": ":material/light_mode:"},
#                     }

st.set_page_config(page_title="GTOME", page_icon=AppIcons.MAIN_APP)
home_page = st.Page("views/home.py", title="Home", icon=AppIcons.HOME_PAGE)
view_page = st.Page("views/dashboard.py", title="Dashboard", icon=AppIcons.DASHBOARD_PAGE)
login_page = st.Page("views/login.py", title="Login", icon=AppIcons.LOG_IN)
error_page = st.Page("views/error.py",title="Error",icon=AppIcons.BUG_REPORT_PAGE,url_path="/error")
authenticated_pages = [home_page,view_page]

try:
    test_supabase_connection()
    if st.session_state.login is True:
        st.query_params.clear()
        st.session_state.sheet_name = set_user_sheet(st.session_state.user_info['email'])
        pg = st.navigation(authenticated_pages,position="hidden")
    else:
        if len(st.query_params.get_all("code")) == 0:
            st.query_params.clear()
        pg = st.navigation([login_page],position="hidden")
    pg.run()
except ConnectionError:
    pg = st.navigation([error_page],position="hidden")
    pg.run()

