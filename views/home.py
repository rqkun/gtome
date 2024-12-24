
import streamlit as st
import lib.authentication as auth
st.markdown(
    """
    ## About
    This is a project for ???.
    The project was built using Python 3 on streamlit with 3 different pages.

    ### Contact:
    - 👾 Github: ([rqkun](https://github.com/rqkun))
"""
)

col1,col2,col3 = st.columns(3)

with col1:
    if st.button("Insert", key="add_direct",type="secondary",icon=":material/add_task:",use_container_width=True):
        st.switch_page("views/add.py")
with col2:
    if st.button("Dashboard", key="view_direct",type="secondary",icon=":material/empty_dashboard:",use_container_width=True):
        st.switch_page("views/view.py")
with col3:
    if st.button("Manage", key="edit_direct",type="secondary",icon=":material/lists:",use_container_width=True):
        st.switch_page("views/manage.py")
with col2:
    if st.button("Logout","", use_container_width=True,type="secondary", icon=":material/exit_to_app:"):
        auth.logout()
