"""Header component for pages. """

import streamlit as st
from classes.messages import AppMessages
import lib.authentication as auth
from classes.icons import AppIcons

def change_lang():
    """ Swap dark/light theme. (Only work correct locally or single user mode) """
    previous_lang = st.session_state.language
    if previous_lang == "en":
        st.session_state.language = "vi"
    elif previous_lang == "vi":
        st.session_state.language = "en"

def add_change_lang():
    """ Add chaneg theme button. (Only work correct locally or single user mode) """
    btn_face = AppIcons.ENGLISH \
        if st.session_state.language == "en" \
            else AppIcons.VIETNAMESE
            
    if st.button(btn_face,on_click=change_lang,use_container_width=True):
        st.rerun()

def add_header():
    """ Add header function. """
    with st.header(""):
        col1, col2,_,col3,col4 = st.columns([1,1,4,1,2])
        if col1.button(":material/home:",type="secondary",use_container_width=True):
            st.switch_page("views/home.py")
        with col2:
            add_change_lang()

        col3.button(":material/exit_to_app:",
                    type="secondary",
                    use_container_width=True,
                    on_click=auth.sign_out)

        with col4:
            with st.popover("Menu",use_container_width=True, icon=AppIcons.MENU_PAGE):
                
                st.page_link("views/dashboard.py",
                             label="Dashboard",
                             icon=AppIcons.DASHBOARD_PAGE,
                             use_container_width=True)
                st.page_link("https://github.com/rqkun/gtome/issues",
                             label="Report",
                             icon=AppIcons.BUG_REPORT_PAGE,
                             use_container_width=True)
def add_error_header():
    """ Add setup header function. """
    with st.header(""):
        _, _,_,_,col4 = st.columns([1,1,4,1,1])
        if col4.button(AppIcons.SYNC,
                    type="secondary",
                    use_container_width=True,help=AppMessages.RELOAD_APP_TOOLTIP
                    ):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.session_state.clear()
            st.rerun()