import streamlit as st

from configs.icons import AppIcons
from configs.messages import AppMessages


def change_language():
    """ Swap language. """
    previous_lang = st.session_state.language
    if previous_lang == "en":
        st.session_state.language = "vi"
    elif previous_lang == "vi":
        st.session_state.language = "en"


def change_language_button():
    """ Add language button. """
    btn_face = " EN" \
        if st.session_state.language == "en" \
            else " VI"
    if st.button(AppIcons.LANGUAGE+btn_face,on_click=change_language,use_container_width=True,type="secondary"):
        st.rerun()


def error_page_header():
    """ Add setup header function. """
    with st.header(""):
        col1, _,_,_,col4 = st.columns([1,1,4,1,1])
        with col1:
            change_language_button()
        if col4.button(AppIcons.SYNC,
                    type="secondary",
                    use_container_width=True,help=AppMessages(st.session_state.language).RELOAD_APP_TOOLTIP
                    ):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.session_state.clear()
            st.rerun()


def sign_out_callable() -> None:
    """ Clear everything and signout. """
    st.session_state.clear()
    st.logout()


def hide_streamlit_header_markdown():
    """Hide the Streamlit header. """
    return """
            <style>
                /* Hide the Streamlit header and menu */
                header {visibility: hidden;}
            </style>
        """