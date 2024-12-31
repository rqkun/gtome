""" Datasource management"""

import calendar
from datetime import datetime, timedelta
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np
from classes.icons import AppIcons
from classes.structure import DataStructure
from classes.messages import AppMessages

def set_up_data():
    """ Data Structure """
    return DataStructure.get_option_map(),DataStructure.get_initial_data()

def init_sheet():
    """ Init Sheet. """
    temp_df = pd.DataFrame(columns=DataStructure.get_categories())
    return temp_df.astype(DataStructure.get_convert_dict())

def init_statistic():
    """ Init Statistic Sheet. """
    temp_df = pd.DataFrame(columns=DataStructure.get_statistic_categories())
    return temp_df.astype(DataStructure.get_statistic_dict())


def read_from(conn,option):
    """ Read Sheet. """
    conn = connect_to_gsheet()
    try:
        return clean(conn.read(worksheet=option))
    except Exception as e:
        raise ConnectionError('GoogleSheet', AppMessages.GSHEET_CONNECTION_ERROR) from e

def find_key(list_str, value):
    """ Finding latest key. """
    try:
        return list_str.index(value)
    except ValueError:
        return len(list_str) - 1

def add_from(df):
    """ Update Sheet. """
    conn = connect_to_gsheet()
    try:
        conn.update(
            worksheet="Expenses",
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
            worksheet="Expenses",
            data=save
        )
        
    except ConnectionError as err:
        st.error(AppMessages.get_connection_errors(err.args),icon=AppIcons.ERROR)


def filter(df,span):
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

@st.cache_data
def get_detail_sheets():
    """ Get all or create a new Sheet. """
    conn = connect_to_gsheet()
    
    worksheet_names = []
    for sheet in conn.client._open_spreadsheet(): # type:ignore
        worksheet_names.append(sheet.title)

    if "Expenses" not in worksheet_names:
        return clean(conn.create(
            worksheet="Expenses",
            data=init_sheet(),
        ))
    else:
        return clean(conn.read(worksheet="Expenses"))
