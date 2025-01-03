"""Header component for pages. """

import streamlit as st
import lib.authentication as auth
from classes.icons import AppIcons

# def change_theme():
#     """ Swap dark/light theme. """
#     previous_theme = st.session_state.themes["current_theme"]
#     tdict = st.session_state.themes["light"] \
#       if st.session_state.themes["current_theme"] == "light" else st.session_state.themes["dark"]
#     for vkey, vval in tdict.items():
#         if vkey.startswith("theme"): 
#             st._config.set_option(vkey, vval)

#     st.session_state.themes["refreshed"] = False
#     if previous_theme == "dark":
#         st.session_state.themes["current_theme"] = "light"
#     elif previous_theme == "light":
#         st.session_state.themes["current_theme"] = "dark"

# @st.fragment
# def add_change_theme():
#     """ Add chaneg theme button. """
#     btn_face = st.session_state.themes["light"]["button_face"] \
#       if st.session_state.themes["current_theme"] == "light" \
#         else st.session_state.themes["dark"]["button_face"]
#     st.button(btn_face,on_click=change_theme,use_container_width=True)

#     if st.session_state.themes["refreshed"] is False:
#         st.session_state.themes["refreshed"] = True
#         st.rerun()

def add_header():
    """ Add header function. """
    with st.header(""):
        col1, _,_,col3,col4 = st.columns([1,1,4,1,2])
        if col1.button(":material/home:",type="secondary",use_container_width=True):
            st.switch_page("views/home.py")
        col3.button(":material/exit_to_app:",
                    type="secondary",
                    use_container_width=True,
                    on_click=auth.sign_out)

        with col4:
            with st.popover("Menu",use_container_width=True, icon=AppIcons.MENU_PAGE):
                st.page_link("views/add.py",
                             label="Insert",
                             icon=AppIcons.INSERT_PAGE,
                             use_container_width=True)

                st.page_link("views/dashboard.py",
                             label="Dashboard",
                             icon=AppIcons.DASHBOARD_PAGE,
                             use_container_width=True)
                st.page_link("views/manage.py",
                             label="Manage",
                             icon=AppIcons.MANAGE_PAGE,
                             use_container_width=True)
                st.page_link("https://github.com/rqkun/gtome/issues",
                             label="Report",
                             icon=AppIcons.BUG_REPORT_PAGE,
                             use_container_width=True)
        # with col1:
        #     # Create a toggle button
        #     add_change_theme()

def add_error_header():
    """ Add setup header function. """
    with st.header(""):
        _, _,_,_,col4 = st.columns([1,1,4,1,1])
        if col4.button(AppIcons.SYNC,
                    type="secondary",
                    use_container_width=True,help="Reload the app."
                    ):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.session_state.clear()
            st.rerun()
        # with col1:
        #     # Create a toggle button
        #     add_change_theme()