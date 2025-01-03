""" Simple Login Page. """

import asyncio
import streamlit as st
import lib.authentication as auth
import lib.headers as header
from classes.icons import AppIcons
def get_auth_client():
    authorization_url = asyncio.run(
        auth.get_authorization_url(client=auth.get_google_auth_client(), redirect_url=st.secrets.google_oauth2.redirect_url)
    )
    return authorization_url
    

@st.dialog("Reset Password")
def reset_password():
    """ Reset Email form. """
    reset_form = st.form(key='Reset Password Form',clear_on_submit=False,border=False)
    col_1,col_2 = reset_form.columns([5,2],vertical_alignment="bottom")
    reset_email = col_1.text_input(label='Email')
    send_btn = col_2.form_submit_button("Send",
                                        use_container_width=True,
                                        type= 'primary',
                                        icon=AppIcons.SEND_EMAIL
                                        )
    auth_notification_dialog = reset_form.empty()
    if send_btn:
        with auth_notification_dialog, st.spinner('Sending password reset link'):
            auth.reset_password(reset_email)
        if 'auth_success' in st.session_state:
            auth_notification_dialog.success(st.session_state.auth_success)
            del st.session_state.auth_success
        elif 'auth_warning' in st.session_state:
            auth_notification_dialog.error(st.session_state.auth_warning)
            del st.session_state.auth_warning

@st.dialog("Create your account")
def sign_up():
    """ Signup form. """
    register_form = st.form(key='Signup form',clear_on_submit=False,border=False)
    email = register_form.text_input(label='Email')
    password = register_form.text_input(label='Password',type='password')
    
    register_notification = register_form.empty()
    register_form.write("")
    if register_form.form_submit_button(label='Create Account',
                                    use_container_width=True,
                                    type='primary',
                                    icon=AppIcons.SEND_EMAIL
                                    ):
        with register_notification, st.spinner('Creating account'):
            auth.create_account(email,password)
        if 'auth_success' in st.session_state:
            register_notification.success(st.session_state.auth_success)
            del st.session_state.auth_success
        elif 'auth_warning' in st.session_state:
            register_notification.error(st.session_state.auth_warning)
            del st.session_state.auth_warning
    st.write("")

@st.dialog("Sign in")
def sign_in():
    """ Signin form. """
    login_form = st.form(key='Signin form',clear_on_submit=False,border=False)
    email = login_form.text_input(label='Email')
    password = login_form.text_input(label='Password',type='password')
    
    login_notfication = login_form.empty()
    st.write("")
    if login_form.form_submit_button(label='Sign In',
                                    use_container_width=True,
                                    type='primary',
                                    icon=AppIcons.LOG_IN
                                    ):
        with login_notfication, st.spinner('Signing in'):
            auth.sign_in(email,password)
        if 'auth_success' in st.session_state:
            login_notfication.success(st.session_state.auth_success)
            del st.session_state.auth_success
        elif 'auth_warning' in st.session_state:
            login_notfication.error(st.session_state.auth_warning)
            del st.session_state.auth_warning
    st.write("")

if 'user_info' not in st.session_state:
    _,col2,_ = st.columns([1,2,1])
    _,left,right = col2.columns([1,5,1])
    left.markdown("""<div style="text-align: center;
                        font-size: 50px; font-weight: bold;">GTOME
                    </div>""",unsafe_allow_html=True)
    with right:
        header.add_change_theme()
    col2.write("")
    placeholder = col2.container()
    col2.divider()
    col2.button("Create account",use_container_width=True,on_click=sign_up,type='secondary')
    col2.button("Forget Password",use_container_width=True,on_click=reset_password)
    col2.write("Already have an account ?")
    col2.button("Sign In",use_container_width=True,on_click=sign_in,type="primary")

    with col2, st.spinner("Signing in..."):
        auth.google_authentication(placeholder)

        

