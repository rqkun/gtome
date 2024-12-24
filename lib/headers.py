import streamlit as st

def add_header():
    with st.header(""):
        left, _, right = st.columns([1,4,1])
        if left.button("Menu","", use_container_width=True,type="secondary", icon=":material/menu_open:"):
            st.switch_page("views/home.py")
        if right.button("Logout","", use_container_width=True,type="secondary", icon=":material/exit_to_app:"):
            st.switch_page("views/home.py")