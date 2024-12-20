import streamlit as st
home_page = st.Page("tabs/home.py", title="Home", icon=":material/home:")
connection_page = st.Page("tabs/connection.py", title="Connection", icon=":material/add_circle:")


pg = st.navigation([home_page, connection_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()