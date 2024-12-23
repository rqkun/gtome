import streamlit as st

home_page = st.Page("views/home.py", title="Home", icon=":material/home:")
connection_page = st.Page("views/admin/add.py", title="Add", icon=":material/add_circle:")
edit_page = st.Page("views/admin/manage.py", title="Manage", icon=":material/edit:")


pg = st.navigation([home_page, connection_page,edit_page],position="hidden")
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()