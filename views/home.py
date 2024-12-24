
import streamlit as st

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
    if st.button("Add", key="add_direct",type="secondary",icon=":material/add_task:",use_container_width=True):
        st.switch_page("views/add.py")
with col2:
    if st.button("View", key="view_direct",type="secondary",icon=":material/empty_dashboard:",use_container_width=True):
        st.switch_page("views/view.py")
with col3:
    if st.button("Edit", key="edit_direct",type="secondary",icon=":material/sync:",use_container_width=True):
        st.switch_page("views/manage.py")
    
