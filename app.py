import streamlit as st

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

st.set_page_config(page_title="GTOME", page_icon=":material/edit_square:")
home_page = st.Page("views/home.py", title="Home", icon=":material/home:")
connection_page = st.Page("views/add.py", title="Add", icon=":material/add_circle:")
edit_page = st.Page("views/manage.py", title="Manage", icon=":material/edit:")
view_page = st.Page("views/view.py", title="View", icon=":material/search:")
login_page = st.Page("views/login.py", title="Login", icon=":material/account_circle:")

authenticated_pages = [home_page, connection_page,edit_page,view_page]

if st.session_state.login == True:
    pg = st.navigation(authenticated_pages,position="hidden")
else:
    pg = st.navigation([login_page],position="hidden")

pg.run()