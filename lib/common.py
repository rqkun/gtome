import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd
import numpy as np


def set_up():
    option_map = {
        0: "Food",
        1: "Rent",
        2: "Traverse",
        3: "Subscriptions",
        4: "Misc",
        5: "Fun"
    }
    initial_data = {
        "Date": datetime.today().strftime("%d/%m/%Y"),
        "Food": 0,
        "Rent": 0,
        "Traverse": 0,
        "Subscriptions": 0,
        "Misc": 0,
        "Fun": 0,
        "Note": ""
    }
    return option_map,initial_data

def init_sheet():
    convert_dict = {
                    'Food': int,
                    'Rent': int,
                    'Traverse': int,
                    'Subscriptions': int,
                    'Misc': int,
                    'Fun': int,
                    'Note': str,
                    }
    temp_df = pd.DataFrame(columns=['Date','Food','Rent','Traverse','Subscriptions','Misc','Fun','Note'])
    return temp_df.astype(convert_dict)
    
def clean(input_df):
    input_df["Date"] = pd.to_datetime(input_df['Date'],format='%d/%m/%Y')
    input_df["Note"] = input_df["Note"].replace(np.nan, '', regex=True)
    input_df["Note"] = input_df["Note"].astype(str)
    input_df[["Food","Rent","Traverse","Subscriptions","Misc"]] = input_df[["Food","Rent","Traverse","Subscriptions","Misc"]].fillna(0)
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
