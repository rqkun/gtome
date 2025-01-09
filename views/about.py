""" Homepage. """
import streamlit as st
from classes.messages import AppMessages
import lib.utils as utils
from classes.icons import AppIcons

utils.add_header()
app_lang = AppMessages(st.session_state.language)
st.markdown(f"# {app_lang.ABOUT_DESCRIPTION}")
st.markdown(f"""
    <div style="text-align: justify;">
    {app_lang.APP_DESCRIPTION}
    </div>
    """,unsafe_allow_html=True)

st.markdown(
    f"""
    #### {app_lang.FUNCTION_DESCRIPTIONS}
    """
)
st.write(f"{app_lang.FUNCTION_CARDS_DESCRIPTION}")
with st.expander(app_lang.EXPANDER):
    col1,col2,col3 = st.columns(3)
    with col1:
        with st.container(border=True,key="home_desc_1",height=250):
            if st.button("Dashboard",
                         type="tertiary",
                         icon=AppIcons.DASHBOARD_PAGE,
                         use_container_width=True):
                st.switch_page("views/dashboard.py")
                pass
            st.write(app_lang.DESC_DASHBOARD)
    with col2:
        with st.container(border=True,key="home_desc_2",height=250):
            st.link_button("Issues",
                           url="https://github.com/rqkun/gtome/issues",
                           type="tertiary",
                           icon=AppIcons.BUG_REPORT_PAGE,
                           use_container_width=True)
            st.write(app_lang.DESC_BUG)
    with col3:
        with st.container(border=True,key="home_desc_3",height=250):
            st.button(app_lang.UTIL_DESCRIPTION,
                           type="tertiary",
                           icon=AppIcons.TOOLS,
                           use_container_width=True)
            st.markdown(
                f"""
                - [{AppIcons.LANGUAGE} EN/VI] - {app_lang.DESC_LANG_SWITCH}
                - [{AppIcons.MENU_PAGE} Menu] - {app_lang.DESC_MENU}
                - [{AppIcons.LOG_OUT}] - {app_lang.DESC_LOGOUT}
                """
)
    
