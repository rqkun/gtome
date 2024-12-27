import streamlit as st

from classes.icons import AppIcons

if 'user_info' not in st.session_state:
    st.session_state.login = False

ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "dark",
                    "refreshed": True,
                    
                    "light": {"theme.base": "dark",
                              "button_face": ":material/dark_mode:"},

                    "dark":  {"theme.base": "light",
                              "button_face": ":material/light_mode:"},
                    }

st.set_page_config(page_title="GTOME", page_icon=AppIcons.MAIN_APP)
home_page = st.Page("views/home.py", title="Home", icon=AppIcons.HOME_PAGE)
connection_page = st.Page("views/add.py", title="Add", icon=AppIcons.INSERT_PAGE)
edit_page = st.Page("views/manage.py", title="Manage", icon=AppIcons.MANAGE_PAGE)
view_page = st.Page("views/dashboard.py", title="Dashboard", icon=AppIcons.DASHBOARD_PAGE)
login_page = st.Page("views/login.py", title="Login", icon=":material/account_circle:")

authenticated_pages = [home_page, connection_page,edit_page,view_page]

if st.session_state.login == True:
    pg = st.navigation(authenticated_pages,position="hidden")
else:
    pg = st.navigation([login_page],position="hidden")

pg.run()