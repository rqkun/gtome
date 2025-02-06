""" Simple Login Page. """

import streamlit as st
from classes.messages import AppMessages


if 'language' not in st.session_state or st.session_state.language =="":
    st.session_state.language = "en"
    
app_lang = AppMessages(st.session_state.language)

_,col2,_ = st.columns([2,2,2])
col2.markdown("""<div style="text-align: center;
                    font-size: 50px; font-weight: bold;">GTOME
                </div>""",unsafe_allow_html=True)
col2.write("")
col2.divider()
if col2.button("Sign in with Google",use_container_width=True,type="primary"):
    st.login()
    st.stop()
