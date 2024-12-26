import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd
import numpy as np
from classes.icons import AppIcons
from classes.structure import DataStructure
from classes.messages import AppMessages

def set_up_data():
    return DataStructure.get_option_map(),DataStructure.get_initial_data()

def init_sheet():
    
    temp_df = pd.DataFrame(columns=DataStructure.get_categories())
    return temp_df.astype(DataStructure.get_convert_dict())


def read_from(conn,option):
    try:
        return clean(conn.read(worksheet=option))
    except ConnectionError as err:
        st.error(AppMessages.get_connecition_errors(err.args),icon=AppIcons.ERROR)

def find_key(list_str,value):
    try:
        return list_str.index(value)
    except:
        return len(list_str)-1

def update_from(conn,option,update_df):
    try:
        if update_df is None:
            update_df = st.session_state['sheet']
        conn.update(
            worksheet=option,
            data=update_df
        )
    except ConnectionError as err:
        st.error(AppMessages.get_connecition_errors(err.args),icon=AppIcons.ERROR)


def clean(input_df):
    input_df["Date"] = pd.to_datetime(input_df['Date'],format='%d/%m/%Y')
    input_df["Date"] = input_df["Date"].replace(np.nan, datetime.today().strftime("%d/%m/%Y"), regex=True)
    input_df["Note"] = input_df["Note"].replace(np.nan, '', regex=True)
    input_df["Note"] = input_df["Note"].astype(str)
    input_df[DataStructure.get_categories_numeric()] = input_df[DataStructure.get_categories_numeric()].fillna(0)
    return input_df.reset_index(drop=True)

@st.cache_resource  
def connect_to_gsheet():
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except:
        raise ConnectionError('GoogleSheet',AppMessages.GSHEET_CONNECTION_ERROR)

@st.cache_resource
def get_sheets():
    try:
        conn = connect_to_gsheet()
    except:
        raise ConnectionError(AppMessages.GSHEET_CONNECTION_ERROR)
    worksheet_names = []
    for sheet in conn.client._open_spreadsheet():
        worksheet_names.append(sheet.title)
    today = datetime.today().strftime('%B-%Y')
    
    if worksheet_names.count(today) ==0:
        conn.create(
            worksheet=today,
            data=init_sheet(),
        )
    return conn, worksheet_names
