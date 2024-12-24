import streamlit as st
import lib.authentication as auth

if "login" not in st.session_state:
    st.session_state.login = False

def login():
    auth.login()
    
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
home_page = st.Page("views/home.py", title="Home", icon=":material/home:")
connection_page = st.Page("views/add.py", title="Add", icon=":material/add_circle:")
edit_page = st.Page("views/manage.py", title="Manage", icon=":material/edit:")
view_page = st.Page("views/view.py", title="View", icon=":material/search:")

login_pages = [home_page, connection_page,edit_page,view_page]

if st.session_state.login == True:
    pg = st.navigation(login_pages,position="hidden")
else:
    pg = st.navigation([st.Page(login)],position="hidden")

pg.run()