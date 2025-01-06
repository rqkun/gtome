""" Datasource management"""

import calendar
from datetime import datetime, timedelta
import gspread
import postgrest
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np
from supabase import create_client
from classes.icons import AppIcons
from classes.structure import DataStructure
from classes.messages import AppMessages
import ast
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
        st.error(AppMessages.get_connection_errors(err.args),icon=AppIcons.ERROR)

def create_from(df):
    """ Create Sheet. """
    conn = connect_to_gsheet()
    try:
        return conn.create(
            worksheet=st.session_state.sheet_name,
            data=df
        )
    except ConnectionError as err:
        st.error(AppMessages.get_connection_errors(err.args),icon=AppIcons.ERROR)


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
        st.error(AppMessages.get_connection_errors(err.args),icon=AppIcons.ERROR)


def filter(df,span):
    """ Return data from dataframe that is in a span of time. """
    start_date = span[0]
    end_date = span[1]
    filtered_df = df
    filtered_df["Date"] = pd.to_datetime(filtered_df['Date'],format='%d/%m/%Y')
    if start_date == end_date:
        filtered_df = filtered_df[(filtered_df['Date'].dt.date == start_date)]
    else:
        filtered_df = filtered_df[(filtered_df['Date'].dt.date >= start_date) & (filtered_df['Date'].dt.date <= end_date)]
    return clean(filtered_df)

def clean(input_df):
    """ Clean the dataframe """
    # input_df["Date"] = pd.to_datetime(input_df['Date'],format='%d/%m/%Y')
    input_df = input_df.sort_values(by="Date")
    input_df["Date"] = input_df["Date"].replace(
        np.nan,datetime.today().strftime("%d/%m/%Y"),regex=True)
    input_df["Note"] = input_df["Note"].replace(np.nan, '', regex=True)
    input_df["Note"] = input_df["Note"].astype(str)
    input_df[DataStructure.get_categories_numeric()] = \
        input_df[DataStructure.get_categories_numeric()].fillna(0)
    return input_df.reset_index(drop=True)

def get_metrics(df,start,end):
    """ Get metrics from Sheet. """
    
    df = filter(df,(start.date(),end.date()))
    
    categories = DataStructure.get_categories_numeric()
    totals = df[categories].fillna(0).sum()
    data = DataStructure.get_initial_statistics("sheet",
                                                total= totals.sum(),
                                                highest=df[categories].max(skipna=True)\
                                                                        .fillna(0)\
                                                                        .max(),
                                                highest_category=totals.idxmax(),
                                                highest_category_value=totals.max())
    return data

def get_delta(new_metric, df):
    """ Get delta from old sheet """
    today = datetime.now()
    # Calculate the first day of the current month
    start_date_this_month = today.replace(day=1)
    # Calculate the last day of the previous month
    end_date_last_month = start_date_this_month - timedelta(days=1)
    # Calculate the first day of the previous month
    start_date_last_month = end_date_last_month.replace(day=1)
    
    last_metric = get_metrics(df,start_date_last_month,end_date_last_month)
    
    return new_metric["Total"] - last_metric["Total"], \
            new_metric["Highest"] - last_metric["Highest"], \
                                last_metric["Highest_Category"], \
            new_metric["Highest_Category_Value"]- last_metric["Highest_Category_Value"]

@st.cache_resource
def connect_to_gsheet():
    """ Connection """
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception as e:
        raise ConnectionError('GoogleSheet', AppMessages.GSHEET_CONNECTION_ERROR) from e

def test_connect_to_sheet(link):
    """ Connection """
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        conn.read(
            worksheet = link,
        )
        return True
    except gspread.exceptions.SpreadsheetNotFound:
        return False

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
    conn = connect_to_supabase()
    try:
        conn.table("user_sheet").select("*").execute().data
    except postgrest.exceptions.APIError as e:
        tmp = ast.literal_eval(e.args[0])
        raise ConnectionError("{0}: {1}".format(tmp['message'], tmp['hint']))

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