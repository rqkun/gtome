import streamlit as st

home_page = st.Page("views/home.py", title="Home", icon=":material/home:")
connection_page = st.Page("views/add.py", title="Add", icon=":material/add_circle:")
edit_page = st.Page("views/manage.py", title="Manage", icon=":material/edit:")
view_page = st.Page("views/view.py", title="View", icon=":material/search:")

pg = st.navigation([home_page, connection_page,edit_page,view_page],position="hidden")
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()