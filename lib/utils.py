"""Header component for pages. """

from io import BytesIO
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
from classes.messages import AppMessages
from classes.structure import DataStructure
from classes.icons import AppIcons
from PIL import Image
import requests
from dateutil.relativedelta import relativedelta

def change_lang():
    """ Swap language. """
    previous_lang = st.session_state.language
    if previous_lang == "en":
        st.session_state.language = "vi"
    elif previous_lang == "vi":
        st.session_state.language = "en"

def add_change_lang():
    """ Add language button. """
    btn_face = " EN" \
        if st.session_state.language == "en" \
            else " VI"
    if st.button(AppIcons.LANGUAGE+btn_face,on_click=change_lang,use_container_width=True,type="secondary"):
        st.rerun()
  
def add_error_header():
    """ Add setup header function. """
    with st.header(""):
        col1, _,_,_,col4 = st.columns([1,1,4,1,1])
        with col1:
            add_change_lang()
        if col4.button(AppIcons.SYNC,
                    type="secondary",
                    use_container_width=True,help=AppMessages(st.session_state.language).RELOAD_APP_TOOLTIP
                    ):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.session_state.clear()
            st.rerun()


def clean(input_df):
    """ Clean dataframe.

    Args:
        input_df (DataFrame): Dataframe that needed to be cleaned.

    Returns:
        DataFrame: A cleaned Dataframe.
    """
    # input_df["Date"] = pd.to_datetime(input_df['Date'],format='%d/%m/%Y')
    input_df = input_df.sort_values(by="Date")
    input_df["Date"] = input_df["Date"].replace(
        np.nan,datetime.today().strftime("%d/%m/%Y"),regex=True)
    input_df["Note"] = input_df["Note"].replace(np.nan, '', regex=True)
    input_df["Note"] = input_df["Note"].astype(str)
    input_df["Spent"] = \
        input_df["Spent"].fillna(0)
    return input_df.reset_index(drop=True)


def filter(df, span):
    """ Return data from dataframe that is in a span of time and the data outside the span.

    Args:
        df (DataFrame): Dataframe that needed to be filtered.
        span (tuple): (start_date,end_date).

    Returns:
        DataFrame: A filtered Dataframe.
    """
    start_date = span[0]
    
    end_date = span[1]
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    
    if start_date == end_date:
        filtered_df = df.loc[(df['Date'].dt.date == start_date)]
    else:
        filtered_df = df.loc[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date < end_date)]
    
    remaining_df = df.loc[~df.index.isin(filtered_df.index)]
    
    return clean(filtered_df), clean(remaining_df)



def normal_plot_data(df):
    """ Return dataframe group by date, type for plotly plot.

    Args:
        df (DataFrame): Dataframe that needed to be grouped.

    Returns:
        DataFrame: A grouped Dataframe.
    """
    # Drop the 'Note' column
    df = df.drop(['Note'], axis=1)

    # Convert 'Date' to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

    # Group by 'Date' and 'Type' and sum the 'Spent' values
    grouped_df = df.groupby(['Date', 'Type'])['Spent'].sum().reset_index()

    return grouped_df


def get_metrics(df,start,end):
    """ Get metrics from a dataframe.

    Args:
        df (DataFrame): Dataframe that needed to be calculated.
        start (date): Start date.
        end (date): End date.

    Returns:
        dict: Statistic Object.
    """

    df,_ = filter(df,(start.date(),end.date()))

    totals = df.groupby('Type')['Spent'].sum()
    if totals.empty:
        return DataStructure.get_initial_statistics()
    data = DataStructure.get_initial_statistics("sheet",
                                                total= totals.sum(),
                                                highest=df.groupby('Type')['Spent'].max()\
                                                                        .max(),
                                                highest_category=totals.idxmax(),
                                                highest_category_value=totals.max())
    return data


def get_delta(new_metric, df, span):
    """ Get delta between current metric with metric from a certain span of time.

    Args:
        new_metric (dict): Current metrics dictionary.
        df (DataFrame): The whole dataframe.
        span (tuple): (start_date,end_date).

    Returns:
        dict: Delta mertrics.
    """

    last_metric = get_metrics(df,span[0],span[1])

    return new_metric["Total"] - last_metric["Total"], \
            new_metric["Highest"] - last_metric["Highest"], \
                                last_metric["Highest_Category"], \
            new_metric["Highest_Category_Value"]- last_metric["Highest_Category_Value"]
            
def get_export_data(dataframe,selection):
    """ Return dataframe object of type chosen and that file name.

    Args:
        dataframe (DataFrame): Exported dataframe.
        selection (string): File type.

    Raises:
        ValueError: Unsupported export type.

    Returns:
        tuple: (file,file_name)
    """
    export_types = DataStructure.get_export_type()
    file_extension = export_types.get(selection, ".csv")
    file_name = "{0}_{1}{2}".format(
        st.experimental_user.email.split('@')[0],
        datetime.today().strftime("%d_%m_%Y_%H_%M_%S"),
        file_extension
    )
    dataframe["Date"] = pd.to_datetime(dataframe["Date"]).dt.strftime("%d/%m/%Y")
    if file_extension == ".csv":
        data_export = dataframe.to_csv(index=False).encode("utf-8-sig")
    elif file_extension == ".xlsx":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            dataframe.to_excel(writer, index=False)
        data_export = output.getvalue()
    elif file_extension == ".xml":
        data_export = dataframe.to_xml(index=False).encode("utf-8-sig")
    elif file_extension == ".parquet":
        output = BytesIO()
        dataframe.to_parquet(output, index=False)
        data_export = output.getvalue()
    elif file_extension == ".orc":
        output = BytesIO()
        dataframe.to_orc(output, index=False)
        data_export = output.getvalue()
    else:
        raise ValueError("Unsupported export type")
    
    return data_export, file_name

def raise_detailed_error(request_object):
    """ Get details on http errors.

    Args:
        request_object (json): Json response data.

    Raises:
        requests.exceptions.HTTPError: HTTP error
    """
    try:
        request_object.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(error, request_object.text)

def get_image(user_url):
    """ Get user avatar image from url.

    Args:
        user_url (string): Image url.

    Returns:
        ImageFile: PIL image file.
    """
    try:
        request_object = requests.get(user_url)
        raise_detailed_error(request_object)
        return Image.open(BytesIO(request_object.content))
    except requests.exceptions.HTTPError as err:
        return None


def sign_out() -> None:
    """ Clear everything and signout. """
    st.session_state.clear()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.logout()

def get_start_and_end(time):
    """ Get start and end date of a month.

    Args:
        time (datetime): Time anchor.

    Returns:
        tuple: (start,end)
    """
    start = time.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + relativedelta(months=1)
    return start , end

def get_endtime_of_today():
    """ Get start and end time of today.

    Returns:
        tuple: (start,end)
    """
    today = datetime.today()
    end = today.replace(hour=23, minute=59, second=59, microsecond=999)
    return end

def hide_streamlit_header():
    """Hide the Streamlit header. """
    return """
            <style>
                /* Hide the Streamlit header and menu */
                header {visibility: hidden;}
            </style>
        """