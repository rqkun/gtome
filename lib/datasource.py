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
    """ Set up data for initialization of a spreadsheet.

    Returns:
        tuple: (list,dict).
    """
    return DataStructure.get_option_map(),DataStructure.get_initial_data()

def init_sheet():
    """ Initialize a dataframe.

    Returns:
        DataFrame: A dataframe with defined types.
    """
    temp_df = pd.DataFrame(columns=DataStructure.get_categories())
    return temp_df.astype(DataStructure.get_convert_dict())

def update_from(df:pd.DataFrame):
    """ Update the whole spreadsheet.

    Args:
        df (DataFrame): Dataframe that needed to be update.
    """
    df["Date"] = df["Date"].apply(lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0))
    conn = connect_to_gsheet()
    try:
        conn.update(
            worksheet=st.experimental_user.sub,
            data=df
        )
    except ConnectionError as err:
        st.error(AppMessages(st.session_state.language).get_connection_errors(err.args),icon=AppIcons.ERROR)

def create_from(df):
    """ Create an spreadsheet with user email as name.

    Args:
        df (DataFrame): Dataframe that needed to be created.

    Returns:
        DataFrame: The freshly created dataframe.
    """
    conn = connect_to_gsheet()
    try:
        return conn.create(
            worksheet=st.experimental_user.sub,
            data=df
        )
    except ConnectionError as err:
        st.error(AppMessages(st.session_state.language).get_connection_errors(err.args),icon=AppIcons.ERROR)

@st.cache_resource(show_spinner=False)
def connect_to_gsheet():
    """ Connect to the Google Spreadsheet.

    Raises:
        gspread.exceptions.GSpreadException: General connection exception.

    Returns:
        ConnectionClass@connection_factory: Streamlit Connection.
    """
    try:
        return st.connection("google_api", type=GSheetsConnection)
    except Exception as e:
        raise gspread.exceptions.GSpreadException('GoogleSheet', AppMessages(st.session_state.language).GSHEET_CONNECTION_ERROR) from e

def test_connect_to_sheet():
    """ Testing the connection.

    Returns:
        tuple: (bool,string)
    """
    try:
        conn = st.connection("google_api", type=GSheetsConnection)
        conn.read()
        return True, ""
    except gspread.exceptions.SpreadsheetNotFound as err:
        return False, err

def get_detail_sheets():
    """ Get current user spreadsheet.

    Returns:
        DataFrame: A clean dataframe.
    """
    conn = connect_to_gsheet()
    try:
        return clean(conn.read(
            worksheet=st.experimental_user.sub,
        ))
    except gspread.exceptions.WorksheetNotFound:
        df = init_sheet()
        return create_from(df)