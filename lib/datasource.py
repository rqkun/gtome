""" Datasource management"""

import gspread
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from classes.icons import AppIcons
from classes.structure import DataStructure
from classes.messages import AppMessages

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
            worksheet=st.experimental_user.email,
            data=df
        )
    except ConnectionError as err:
        st.error(AppMessages(st.session_state.language).get_connection_errors(err.args),icon=AppIcons.ERROR)

def create_from(df):
    """ Create Sheet. """
    conn = connect_to_gsheet()
    try:
        return conn.create(
            worksheet=st.experimental_user.email,
            data=df
        )
    except ConnectionError as err:
        st.error(AppMessages(st.session_state.language).get_connection_errors(err.args),icon=AppIcons.ERROR)


def update_from(original_df):#updated_df,old_df,sheet
    """ Update Sheet that include another dataframe. """
    conn = connect_to_gsheet()
    try:
        conn.update(
            worksheet=st.experimental_user.email,
            data=original_df
        )
        
    except ConnectionError as err:
        st.error(AppMessages(st.session_state.language).get_connection_errors(err.args),icon=AppIcons.ERROR)

@st.cache_resource(show_spinner=False)
def connect_to_gsheet():
    """ Connection """
    try:
        return st.connection("google_api", type=GSheetsConnection)
    except Exception as e:
        raise gspread.exceptions.GSpreadException('GoogleSheet', AppMessages(st.session_state.language).GSHEET_CONNECTION_ERROR) from e

def test_connect_to_sheet():
    """ Connection """
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
            worksheet=st.experimental_user.email,
        ))
    except gspread.exceptions.WorksheetNotFound:
        df = init_sheet()
        return create_from(df)