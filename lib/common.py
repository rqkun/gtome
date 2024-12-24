import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd
import numpy as np
from lib.classes import DataStructure


def set_up():
    return DataStructure.get_option_map(),DataStructure.get_initial_data()

def init_sheet():
    
    temp_df = pd.DataFrame(columns=DataStructure.get_categories())
    return temp_df.astype(DataStructure.get_convert_dict())


def find_key(list_str,value):
    try:
        return list_str.index(value)
    except:
        return len(list_str)-1


def clean(input_df):
    input_df["Date"] = pd.to_datetime(input_df['Date'],format='%d/%m/%Y')
    input_df["Note"] = input_df["Note"].replace(np.nan, '', regex=True)
    input_df["Note"] = input_df["Note"].astype(str)
    input_df[DataStructure.get_categories_numeric()] = input_df[DataStructure.get_categories_numeric()].fillna(0)
    return input_df.reset_index(drop=True)

@st.cache_resource  
def connect_to_gsheet():
    return st.connection("gsheets", type=GSheetsConnection)

@st.cache_resource
def get_sheets():
    conn = connect_to_gsheet()
    worksheet_names = []
    for sheet in conn.client._open_spreadsheet():
        worksheet_names.append(sheet.title)
    today = datetime.today().strftime('%B-%Y')
    
    if worksheet_names.count(today) ==0:
        connect_to_gsheet().create(
            worksheet=today,
            data=init_sheet(),
        )
    return conn, worksheet_names
