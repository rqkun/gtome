""" Simple Login Page. """

import streamlit as st
from configs.icons import AppIcons
from configs.messages import AppMessages
from components import custom_components


if 'language' not in st.session_state or st.session_state.language =="":
    st.session_state.language = "en"
    
app_lang = AppMessages(st.session_state.language)

_,col2,_ = st.columns(3)


col2.markdown("""<div style="text-align: center;
                    font-size: 50px; font-weight: bold;">GTOME
                </div>""",unsafe_allow_html=True)

col2.image("https://i.natgeofe.com/n/8271db90-5c35-46bc-9429-588a9529e44a/raccoon_thumb_square.JPG?wp=1&w=357&h=357",use_container_width=True,caption="Financial Management")
# col2.divider()
left,right = col2.columns([1.2,2])
with left:
    custom_components.change_language_button()
if right.button(app_lang.SIGN_IN,use_container_width=True,type="primary",icon=AppIcons.LOG_IN, help=app_lang.SIGN_IN_GOOGLE):
    st.login()
    st.stop()
