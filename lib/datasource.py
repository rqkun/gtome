""" Datasource management"""

from datetime import datetime
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

def update_from(conn,option,update_df):
    """ Update Sheet. """
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
    """ Clean the dataframe """
    input_df["Date"] = pd.to_datetime(input_df['Date'],format='%d/%m/%Y')
    input_df = input_df.sort_values(by="Date")
    input_df["Date"] = input_df["Date"].replace(
        np.nan,datetime.today().strftime("%d/%m/%Y"),regex=True)
    input_df["Note"] = input_df["Note"].replace(np.nan, '', regex=True)
    input_df["Note"] = input_df["Note"].astype(str)
    input_df[DataStructure.get_categories_numeric()] = \
        input_df[DataStructure.get_categories_numeric()].fillna(0)
    return input_df.reset_index(drop=True)

def get_metrics(sheet):
    """ Get metrics from Sheet. """
    conn = connect_to_gsheet()
    temp = conn.read(worksheet=sheet)
    categories = DataStructure.get_categories_numeric()
    totals = temp[categories].fillna(0).sum()
    data = DataStructure.get_initial_statistics(sheet,
                                                total= totals.sum(),
                                                highest=temp[categories].max(skipna=True)\
                                                                        .fillna(0)\
                                                                        .max(),
                                                highest_category=totals.idxmax(),
                                                highest_category_value=totals.max())
    return data

def get_delta(data):
    """ Get delta from old sheet """
    conn = connect_to_gsheet()
    stats = conn.read(worksheet="Statistics")
    index = stats.index[stats['Sheet'] == data['Sheet']].tolist()[0]
    if index > 0:
        last_metric = stats.iloc[index - 1]
    else:
        last_metric = DataStructure.get_initial_statistics()

    return data["Total"] - last_metric["Total"], \
            data["Highest"] - last_metric["Highest"], \
                                last_metric["Highest_Category"], \
            data["Highest_Category_Value"]- last_metric["Highest_Category_Value"]
@st.cache_resource
def connect_to_gsheet():
    """ Connection """
    try:
        return st.connection("gsheets", type=GSheetsConnection)
    except Exception as e:
        raise ConnectionError('GoogleSheet', AppMessages.GSHEET_CONNECTION_ERROR) from e

@st.cache_resource
def get_detail_sheets():
    """ Get all or create a new Sheet. """
    conn = connect_to_gsheet()
    worksheet_names = []
    for sheet in conn.client._open_spreadsheet():
        if sheet.title != "Statistics":
            worksheet_names.append(sheet.title)

    today = datetime.today().strftime('%B-%Y')
    if today not in worksheet_names:
        conn.create(
            worksheet=today,
            data=init_sheet(),
        )

    return conn, worksheet_names


@st.cache_resource
def get_statistic_sheet():
    """ Get/Create a Statistic Sheet. """
    conn = connect_to_gsheet()
    worksheet_names = []
    for sheet in conn.client._open_spreadsheet():
        worksheet_names.append(sheet.title)

    data = init_statistic()
    for title in worksheet_names:
        if title != "Statistics":
            init_data = get_metrics(title)
            data.loc[len(data)] = init_data

    if "Statistics" not in worksheet_names:
        conn.create(
            worksheet="Statistics",
            data=data,
        )
    else:
        conn.update(
            worksheet="Statistics",
            data=data,
        )
    