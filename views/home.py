from streamlit_extras.button_selector import button_selector 
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

def example():
    month_list = [
        "Add",
        "View",
        "Edit"
    ]
    selected_index = button_selector(
        month_list,
        index=0,
        spec=3,
        key="button_selector_example_month_selector",
        label="Month Selector",
    )
    #st.write(f"Selected month: {month_list[selected_index]}")
    if month_list[selected_index] == "Add":
        st.switch_page("views/add.py")
    if month_list[selected_index] == "View":
        st.switch_page("views/view.py")
    if month_list[selected_index] == "Edit":
        st.switch_page("views/manage.py")
example()