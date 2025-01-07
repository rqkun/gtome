""" Firebase API Authentication. """
import json
import re
import streamlit as st
import requests
from classes.messages import AppMessages

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import streamlit as st

from lib import custom_components

## -------------------------------------------------------------------------------------------------
## Firebase Auth API -------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------

def sign_in_with_external(id_token):
    """ Sending GoogleAPI signInWithIdp API for signing in with Google. """
    request_ref = "{0}/verifyAssertion?key={1}".format(st.secrets.connections.google_api.endpoint,st.secrets.connections.google_api.api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({
        'postBody': f'id_token={id_token}&providerId=google.com',
        'requestUri': st.secrets.connections.google_api.redirect_url,
        'returnIdpCredential': True,
        'returnSecureToken': True
    })
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()


def sign_in_with_email_and_password(email, password):
    """ Sending GoogleAPI verifyPassword API for signing in with Email, Password. """
    request_ref = "{0}/verifyPassword?key={1}".format(st.secrets.connections.google_api.endpoint,st.secrets.connections.google_api.api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def get_account_info(id_token):
    """ Sending GoogleAPI getAccountInfo API for account info. """
    request_ref = "{0}/getAccountInfo?key={1}".format(st.secrets.connections.google_api.endpoint,st.secrets.connections.google_api.api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"idToken": id_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def send_email_verification(id_token):
    """ Sending GoogleAPI getAccountInfo API for sending email verification. """
    request_ref = "{0}/getOobConfirmationCode?key={1}".format(st.secrets.connections.google_api.endpoint,st.secrets.connections.google_api.api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"requestType": "VERIFY_EMAIL", "idToken": id_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def send_password_reset_email(email):
    """ Sending GoogleAPI getAccountInfo API for sending reset password email. """
    request_ref = "{0}/getOobConfirmationCode?key={1}".format(st.secrets.connections.google_api.endpoint,st.secrets.connections.google_api.api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def create_user_with_email_and_password(email, password):
    """ Sending GoogleAPI getAccountInfo API for creating user. """
    request_ref = "{0}/signupNewUser?key={1}".format(st.secrets.connections.google_api.endpoint,st.secrets.connections.google_api.api_key)
    headers = {"content-type": "application/json; charset=UTF-8" }
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def delete_user_account(id_token):
    """ Sending GoogleAPI getAccountInfo API for deleting user. """
    request_ref = "{0}/deleteAccount?key={1}".format(st.secrets.connections.google_api.endpoint,st.secrets.connections.google_api.api_key)
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"idToken": id_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def raise_detailed_error(request_object):
    """ Get details on http errors. """
    try:
        request_object.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(error, request_object.text)

## -------------------------------------------------------------------------------------------------
## Authentication functions ------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------

def sign_in(email:str, password:str) -> None:
    """ Sign in with email & password. """
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
        st.session_state.auth_warning = AppMessages.INTERNAL_SERVER_ERROR + "".join(error.args)


## -------------------------------------------------------------------------------------------------
## OAuth2 API --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------

def google_authentication(component):
    """ Sign in with OAuth (Google). """
    try:
        auth_code = st.query_params.get("code")
        CLIENT_CONFIG = {'web': {
            'client_id': st.secrets.connections.google_api.client_id,
            'project_id': st.secrets.connections.google_api.project_id,
            'auth_uri': st.secrets.connections.google_api.auth_uri,
            'token_uri': st.secrets.connections.google_api.token_uri,
            'auth_provider_x509_cert_url': st.secrets.connections.google_api.auth_provider_x509_cert_url,
            'client_secret': st.secrets.connections.google_api.secret,
            'redirect_uris': st.secrets.connections.google_api.redirect_url,
            'javascript_origins': st.secrets.connections.google_api.javascript_origins
        }}
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            CLIENT_CONFIG, # replace with you json credentials from your google auth app
            scopes=["https://www.googleapis.com/auth/userinfo.email", "openid"],
            redirect_uri=st.secrets.connections.google_api.redirect_url,
        )
        if auth_code:
            custom_components.google_sign_in_button(component,url="")
            
            flow.fetch_token(code=auth_code)
            credentials = flow.credentials
            user_info_service = build(
                serviceName="oauth2",
                version="v2",
                credentials=credentials,
            )
            
            user_info = user_info_service.userinfo().get().execute()
            assert user_info.get("email"), "Email not found in infos"
            response = sign_in_with_external(credentials.id_token)
            
            if 'error' in response:
                raise requests.exceptions.HTTPError(f"{AppMessages.FIREBASE_CONNECTION_ERROR}: {response['error']['message']}")
            
            st.session_state["google_auth_code"] = auth_code
            st.session_state.user_info = user_info
            st.session_state.login = True
            st.query_params.clear()
            st.rerun()
        else:
            st.query_params.clear()
            authorization_url, state = flow.authorization_url(
                access_type="offline",
                include_granted_scopes="true",
            )
            custom_components.google_sign_in_button(component,url=authorization_url)
            
    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        st.session_state.auth_warning = error_message

    except Exception as error:
        st.session_state.auth_warning = AppMessages.INTERNAL_SERVER_ERROR + "".join(error.args)




def password_warning_builder(str):
    """ Password requirement parser. """
    requirements_part = re.search(r'\[(.*?)\]', str).group(1)
    requirements_list = [req.strip() for req in requirements_part.split(',')]
    formatted_requirements = ', '.join([req.replace('Password must contain', '') for req in requirements_list])
    return f"{AppMessages.WEAK_PASSWORD} {formatted_requirements}."


def create_account(email:str, password:str) -> None:
    """ Create account with email & password. """
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
    """ Send reset password email. """
    try:
        send_password_reset_email(email)
        st.session_state.auth_success = AppMessages.RESET_EMAIL_SENT
    
    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        if error_message in {"MISSING_EMAIL","INVALID_EMAIL","EMAIL_NOT_FOUND"}:
            st.session_state.auth_warning = AppMessages.INVALID_EMAIL
        else:
            st.session_state.auth_warning = error_message
    
    except Exception as error:
        st.session_state.auth_warning = AppMessages.INTERNAL_SERVER_ERROR + "".join(error.args)


def sign_out() -> None:
    """ Clear everything and signout. """
    st.session_state.clear()
    st.cache_data.clear()
    st.cache_resource.clear()

def delete_account(password:str) -> None:
    """ Delete account button. """
    try:
        # Confirm email and password by signing in (and save id_token)
        id_token = sign_in_with_email_and_password(st.session_state.user_info['email'],password)['idToken']
        
        # Attempt to delete account
        delete_user_account(id_token)
        st.session_state.clear()
        st.session_state.auth_success = AppMessages.ACCOUNT_DELETED

    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        st.session_state.auth_warning = error_message
    except Exception as error:
        st.session_state.auth_warning = AppMessages.INTERNAL_SERVER_ERROR + "".join(error.args)