""" Simple Login Page. """

import streamlit as st
import lib.authentication as auth
import lib.headers as header
from classes.icons import AppIcons
@st.dialog("Reset Password")
def reset_password(reset_email):
    """ Reset Email form. """
    reset_form = st.form(key='Reset Password Form',clear_on_submit=False,border=False)
    col_1,col_2 = reset_form.columns([5,2],vertical_alignment="bottom")
    reset_email = col_1.text_input(label='Email',value=reset_email)
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

if 'user_info' not in st.session_state:
    _,col2,_ = st.columns([1,2,1])
    _,left,right = col2.columns([1,5,1])
    with right:
        header.add_change_theme()
    left.markdown("""<div style="text-align: center;
                        font-size: 50px; font-weight: bold;">GTOME
                    </div>""",unsafe_allow_html=True)
    # Authentication form layout
    auth_form = col2.form(key='Authentication form',clear_on_submit=False,border=False)
    email = auth_form.text_input(label='Email')
    password = auth_form.text_input(label='Password',type='password')
    register = col2.toggle("Don't have an account? Click to register.")
    auth_notification = auth_form.empty()
    bot_left,bot_right = col2.columns([3,2],vertical_alignment="center")
    bot_left.write("Forgot your password?")

    if bot_right.button("Reset",type= "secondary",use_container_width=True,icon=AppIcons.MAIL):
        reset_password(email)
    if register and auth_form.form_submit_button(label='Create Account',
                                                 use_container_width=True,
                                                 type='primary',
                                                 icon=AppIcons.SEND_EMAIL
                                                 ):
        with auth_notification, st.spinner('Creating account'):
            auth.create_account(email,password)
     # Sign In
    elif register is False and auth_form.form_submit_button(label='Sign In',
                                                            use_container_width=True,
                                                            type='primary',
                                                            icon=AppIcons.LOG_IN
                                                            ):
        with auth_notification, st.spinner('Signing in'):
            auth.sign_in(email,password)


    # Authentication success and warning messages
    if 'auth_success' in st.session_state:
        auth_notification.success(st.session_state.auth_success)
        del st.session_state.auth_success
    elif 'auth_warning' in st.session_state:
        auth_notification.error(st.session_state.auth_warning)
        del st.session_state.auth_warning
