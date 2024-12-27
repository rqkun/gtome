""" Firebase API Authentication. """
import json
import re
import streamlit as st
import requests
from classes.messages import AppMessages
## -------------------------------------------------------------------------------------------------
## Firebase Auth API -------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------

def sign_in_with_email_and_password(email, password):
    """ Fire"""
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(st.secrets.firebase.api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def get_account_info(id_token):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={0}".format(st.secrets.firebase.api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"idToken": id_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def send_email_verification(id_token):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(st.secrets.firebase.api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"requestType": "VERIFY_EMAIL", "idToken": id_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def send_password_reset_email(email):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(st.secrets.firebase.api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def create_user_with_email_and_password(email, password):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={0}".format(st.secrets.firebase.api_key)
    headers = {"content-type": "application/json; charset=UTF-8" }
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def delete_user_account(id_token):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/deleteAccount?key={0}".format(st.secrets.firebase.api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"idToken": id_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def raise_detailed_error(request_object):
    try:
        request_object.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(error, request_object.text)

## -------------------------------------------------------------------------------------------------
## Authentication functions ------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------

def sign_in(email:str, password:str) -> None:
    try:
        # Attempt to sign in with email and password
        id_token = sign_in_with_email_and_password(email,password)['idToken']

        # Get account information
        user_info = get_account_info(id_token)["users"][0]

        # If email is not verified, send verification email and do not sign in
        if not user_info["emailVerified"]:
            send_email_verification(id_token)
            st.session_state.auth_warning = AppMessages.MAIL_NOT_VERIFY

        # Save user info to session state and rerun
        else:
            st.session_state.user_info = user_info
            st.session_state.login = True
            st.rerun()

    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        if error_message in {"INVALID_EMAIL","INVALID_PASSWORD","MISSING_PASSWORD","INVALID_LOGIN_CREDENTIALS"}:
            st.session_state.auth_warning = AppMessages.INVALID_LOGIN_CREDENTIALS
        else:
            st.session_state.auth_warning = error_message

    except Exception as error:
        print(error)
        st.session_state.auth_warning = AppMessages.INTERNAL_SERVER_ERROR + "".join(error.args)


def password_warning_builder(str):
    requirements_part = re.search(r'\[(.*?)\]', str).group(1)
    requirements_list = [req.strip() for req in requirements_part.split(',')]
    formatted_requirements = ', '.join([req.replace('Password must contain', '') for req in requirements_list])
    return "Password must contain: " + formatted_requirements + "."


def create_account(email:str, password:str) -> None:
    try:
        # Create account (and save id_token)
        id_token = create_user_with_email_and_password(email,password)['idToken']

        # Create account and send email verification
        send_email_verification(id_token)
        st.session_state.auth_success = AppMessages.VERIFY_EMAIL_SENT
    
    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        if error_message == "EMAIL_EXISTS":
            st.session_state.auth_warning = AppMessages.EMAIL_EXIST
        elif error_message in {"INVALID_EMAIL","INVALID_PASSWORD","MISSING_PASSWORD","MISSING_EMAIL"}:
            st.session_state.auth_warning = AppMessages.INVALID_LOGIN_CREDENTIALS
        elif "PASSWORD_DOES_NOT_MEET_REQUIREMENTS" in error_message:
            st.session_state.auth_warning = password_warning_builder(error_message)
        else:
            st.session_state.auth_warning = error_message
    
    except Exception as error:
        print(error)
        st.session_state.auth_warning = AppMessages.INTERNAL_SERVER_ERROR + "".join(error.args)


def reset_password(email:str) -> None:
    try:
        send_password_reset_email(email)
        st.session_state.auth_success = AppMessages.RESET_EMAIL_SENT
    
    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        if error_message in {"MISSING_EMAIL","INVALID_EMAIL","EMAIL_NOT_FOUND"}:
            st.session_state.auth_warning = 'Error: Use a valid email'
        else:
            st.session_state.auth_warning = error_message
    
    except Exception as error:
        st.session_state.auth_warning = AppMessages.INTERNAL_SERVER_ERROR + "".join(error.args)


def sign_out() -> None:
    st.session_state.clear()
    st.session_state.auth_success = AppMessages.SIGN_OUT


def delete_account(password:str) -> None:
    try:
        # Confirm email and password by signing in (and save id_token)
        id_token = sign_in_with_email_and_password(st.session_state.user_info['email'],password)['idToken']
        
        # Attempt to delete account
        delete_user_account(id_token)
        st.session_state.clear()
        st.session_state.auth_success = AppMessages.ACCOUNT_DELETED

    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        print(error_message)

    except Exception as error:
        st.session_state.auth_warning = AppMessages.INTERNAL_SERVER_ERROR + "".join(error.args)