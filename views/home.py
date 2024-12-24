
import streamlit as st
import lib.headers as header

header.add_header()

st.header("About")
st.markdown("""
    <div style="text-align: justify;">
    A user-friendly Streamlit app designed to streamline your financial management. \
    By seamlessly importing data from Google Sheets, it allows you to track expenses, manage budgets, and generate insightful financial reports. \
    With intuitive visualizations, the app helps you stay on top of your finances effortlessly.
    </div>
    """,unsafe_allow_html=True)

st.markdown(
    """
    ### Description
    """
)
st.write("Below are the cards explaining what each of the functions are.")
with st.expander("See explanation"):
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        with st.container(border=True,key="home_desc_1"):
            if st.button("Insert",type="tertiary",icon=":material/add_task:",use_container_width=True):
                st.switch_page("views/add.py")
            st.write("View/Add entries to your expenses reports.")
    with col2:
        with st.container(border=True,key="home_desc_2"):
            if st.button("Dashboard",type="tertiary",icon=":material/empty_dashboard:",use_container_width=True):
                st.switch_page("views/view.py")
            st.write("Metrics, charts from your expenses reports.")
    with col3:
        with st.container(border=True,key="home_desc_3"):
            if st.button("Manage",type="tertiary",icon=":material/lists:",use_container_width=True):
                st.switch_page("views/manage.py")
            st.write("Add/edit/delete multiple entries in reports.")
    with col4:
        with st.container(border=True,key="home_desc_4"):
            st.link_button("Report",url="https://github.com/rqkun/gtome/issues",type="tertiary",icon=":material/bug_report:",use_container_width=True)
            st.write("Report bugs in our github repo's issue page.")
    st.markdown(
    """
    ###### Utilities:
    - [:material/dark_mode: / :material/light_mode:] - Toggle light/dark mode.
    - [:material/exit_to_app: Logout] - Logout.
    - [:material/menu: Menu] - Navigation menu.
    """
)

st.markdown(
    """
    ### Contact:
    - 👾 Github: ([rqkun](https://github.com/rqkun))
    """
)