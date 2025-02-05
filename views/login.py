""" Simple Login Page. """

import asyncio
import streamlit as st
from classes.messages import AppMessages
from lib import utils
import lib.authentication as auth
from classes.icons import AppIcons


if 'language' not in st.session_state or st.session_state.language =="":
    st.session_state.language = "en"
    
app_lang = AppMessages(st.session_state.language)

def get_auth_client():
    """ Initalize an google authentication client. """
    authorization_url = asyncio.run(
        auth.get_authorization_url(client=auth.get_google_auth_client(), redirect_url=st.secrets.google_oauth2.redirect_url)
    )
    return authorization_url
    

@st.dialog(app_lang.FORGET_PASSWORD_FORM)
def reset_password():
    """ Reset Email form. """
    reset_form = st.form(key='Reset Password Form',clear_on_submit=False,border=False)
    col_1,col_2 = reset_form.columns([5,2],vertical_alignment="bottom")
    reset_email = col_1.text_input(label='Email')
    send_btn = col_2.form_submit_button(app_lang.SEND_BUTTON,
                                        use_container_width=True,
                                        type= 'primary',
                                        icon=AppIcons.SEND_EMAIL
                                        )
    auth_notification_dialog = reset_form.empty()
    if send_btn:
        with auth_notification_dialog, st.spinner(app_lang.SENDING_RESET_EMAIL):
            auth.reset_password(reset_email)
        if 'auth_success' in st.session_state:
            auth_notification_dialog.success(st.session_state.auth_success, icon= AppIcons.SUCCESS)
            del st.session_state.auth_success
        elif 'auth_warning' in st.session_state:
            auth_notification_dialog.error(st.session_state.auth_warning, icon= AppIcons.ERROR)
            del st.session_state.auth_warning

@st.dialog(app_lang.CREATE_ACCOUNT_FORM)
def sign_up():
    """ Signup form. """
    register_form = st.form(key='Signup form',clear_on_submit=False,border=False)
    email = register_form.text_input(label='Email')
    password = register_form.text_input(label=app_lang.PASSWORD_TOOLTIP,type='password')
    
    register_notification = register_form.empty()
    register_form.write("")
    if register_form.form_submit_button(label=app_lang.CREATE_ACCOUNT,
                                    use_container_width=True,
                                    type='primary',
                                    icon=AppIcons.SEND_EMAIL
                                    ):
        with register_notification, st.spinner(app_lang.SENDING_SIGNUP_EMAIL):
            auth.create_account(email,password)
        if 'auth_success' in st.session_state:
            register_notification.success(st.session_state.auth_success, icon= AppIcons.SUCCESS)
            del st.session_state.auth_success
        elif 'auth_warning' in st.session_state:
            register_notification.error(st.session_state.auth_warning, icon= AppIcons.ERROR)
            del st.session_state.auth_warning
    st.write("")

@st.dialog(app_lang.SIGN_IN_FORM)
def sign_in():
    """ Signin form. """
    login_form = st.form(key='Signin form',clear_on_submit=False,border=False)
    email = login_form.text_input(label='Email')
    password = login_form.text_input(label=app_lang.PASSWORD_TOOLTIP,type='password')
    
    login_notfication = login_form.empty()
    st.write("")
    if login_form.form_submit_button(label=app_lang.SIGN_IN,
                                    use_container_width=True,
                                    type='primary',
                                    icon=AppIcons.LOG_IN
                                    ):
        with login_notfication, st.spinner(app_lang.SIGN_IN_LOAD_TOOLTIP):
            auth.sign_in(email,password)
        if 'auth_success' in st.session_state:
            login_notfication.success(st.session_state.auth_success, icon= AppIcons.SUCCESS)
            del st.session_state.auth_success
        elif 'auth_warning' in st.session_state:
            login_notfication.error(st.session_state.auth_warning, icon= AppIcons.ERROR)
            del st.session_state.auth_warning
    st.write("")

# if 'user_info' not in st.session_state:
#     _,col2,_ = st.columns([2,2,2])
#     col2.markdown("""<div style="text-align: center;
#                         font-size: 50px; font-weight: bold;">GTOME
#                     </div>""",unsafe_allow_html=True)
#     col2.write("")
#     placeholder = col2.container()
#     col2.divider()
#     col2.button(app_lang.CREATE_ACCOUNT,use_container_width=True,on_click=sign_up,type='secondary')
#     col2.button(app_lang.FORGET_PASSWORD,use_container_width=True,on_click=reset_password)
#     left,right = col2.columns([4,2],vertical_alignment="center")
#     left.write(app_lang.SIGN_IN_TOOLTIP)
#     with right:
#         utils.add_change_lang()
#     col2.button(app_lang.SIGN_IN,use_container_width=True,on_click=sign_in,type="primary")
#     with col2, st.spinner(app_lang.SIGN_IN_LOAD_TOOLTIP):
#         auth.google_authentication(placeholder)
#     if 'auth_success' in st.session_state:
#         st.toast(st.session_state.auth_success, icon= AppIcons.SUCCESS)
#         del st.session_state.auth_success
#     elif 'auth_warning' in st.session_state:
#         st.toast(st.session_state.auth_warning, icon= AppIcons.ERROR)
#         del st.session_state.auth_warning

    
    

        
# if not st.experimental_user.is_logged_in:
_,col2,_ = st.columns([2,2,2])
col2.markdown("""<div style="text-align: center;
                    font-size: 50px; font-weight: bold;">GTOME
                </div>""",unsafe_allow_html=True)
col2.write("")
col2.divider()
if col2.button("Sign in with Google",use_container_width=True,type="primary"):
    st.login()
    st.stop()
