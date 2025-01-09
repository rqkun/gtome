""" Datasource management"""

import calendar
import gspread
import postgrest
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from supabase import create_client
from classes.icons import AppIcons
from classes.structure import DataStructure
from classes.messages import AppMessages
import ast

from lib.utils import clean
def set_up_data():
    """ Data Structure """
    return DataStructure.get_option_map(),DataStructure.get_initial_data()

def init_sheet():
    """ Init Sheet. """
    temp_df = pd.DataFrame(columns=DataStructure.get_categories())
    return temp_df.astype(DataStructure.get_convert_dict())

def add_from(df):
    """ Update Sheet. """
    conn = connect_to_gsheet()
    try:
        conn.update(
            worksheet=st.session_state.sheet_name,
            data=df
        )
    except ConnectionError as err:
        st.error(AppMessages(st.session_state.language).get_connection_errors(err.args),icon=AppIcons.ERROR)

def create_from(df):
    """ Create Sheet. """
    conn = connect_to_gsheet()
    try:
        return conn.create(
            worksheet=st.session_state.sheet_name,
            data=df
        )
    except ConnectionError as err:
        st.error(AppMessages(st.session_state.language).get_connection_errors(err.args),icon=AppIcons.ERROR)


def update_from(updated_df,old_df,sheet):
    """ Update Sheet that include another dataframe. """
    conn = connect_to_gsheet()
    try:
        sheet = sheet[~sheet.apply(tuple,1).isin(old_df.apply(tuple,1))]

        save = pd.concat([sheet, updated_df], ignore_index= True)
        save = clean(save)
        conn.update(
            worksheet=st.session_state.sheet_name,
            data=save
        )
        
    except ConnectionError as err:
        st.error(AppMessages(st.session_state.language).get_connection_errors(err.args),icon=AppIcons.ERROR)

@st.cache_resource
def connect_to_gsheet():
    """ Connection """
    try:
        return st.connection("google_api", type=GSheetsConnection)
    except Exception as e:
        raise ConnectionError('GoogleSheet', AppMessages(st.session_state.language).GSHEET_CONNECTION_ERROR) from e

def test_connect_to_sheet():
    """ Connection """
    st.cache_resource.clear()
    try:
        conn = st.connection("google_api", type=GSheetsConnection)
        conn.read()
        return True, ""
    except gspread.exceptions.SpreadsheetNotFound as err:
        return False, err

def get_detail_sheets():
    """ Get all or create a new Sheet. """
    conn = connect_to_gsheet()
    try:
        return clean(conn.read(
            worksheet=st.session_state.sheet_name,
        ))
    except gspread.exceptions.WorksheetNotFound:
        df = init_sheet()
        return create_from(df)

#----------------------
#   Supabase
#----------------------

def test_supabase_connection():
    """ Connection """
    st.cache_resource.clear()
    conn = connect_to_supabase()
    try:
        conn.table("user_sheet").select("*").execute().data
        return True, ""
    except postgrest.exceptions.APIError as e:
        tmp = ast.literal_eval(e.args[0])
        return False, "{0}: {1}".format(tmp['message'], tmp['hint'])

@st.cache_resource
def connect_to_supabase():
    """ Connection """
    url = st.secrets.supabase.url
    key = st.secrets.supabase.key
    return create_client(url, key)

def get_user_sheet(email):
    """ Get all user sheets. """
    conn = connect_to_supabase()
    try:
        data = conn.table("user_sheet").select("*").like_all_of("email",email).execute().data
        if len(data) == 0:
            return ""
        else: 
            return data[0]['sheet']
    except postgrest.exceptions.APIError as e:
        tmp = ast.literal_eval(e.args[0])
        raise ConnectionError("{0}: {1}".format(tmp['message'], tmp['hint']))

def set_user_sheet(email):
    """ Set user sheet or insert new user sheet"""
    sheet = check_exist(email)
    conn = connect_to_supabase()
    if sheet is None:
        response = (
            conn.table("user_sheet")
            .insert({"email": email})
            .execute()
        )
    else: 
        response = (
            conn.table("user_sheet")
            .select("*")
            .eq("email", email)
            .execute()
        )
    return response.data[0]['sheet']

def check_exist(user):
    """ Check supabase user db."""
    conn = connect_to_supabase()
    response = (
            conn.table("user_sheet")
            .select("*")
            .eq("email",user)
            .execute()
        )
    if len(response.data) > 0:
        return response.data[0]['sheet']
    else:
        return None