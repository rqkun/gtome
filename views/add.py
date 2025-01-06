"""The Insert Page for Data Ingestion."""

import calendar
from datetime import datetime
import pandas as pd
import streamlit as st
import lib.datasource as datasource
import lib.headers as header
from classes.messages import AppMessages
from classes.icons import AppIcons

@st.dialog("Insert Data")
def insert(df):
    """
        Create a insert dialog form
    """
    try:
        option_map, initial_data = datasource.set_up_data()
        amount = st.number_input("Amount",min_value=0,
                                 step=1000,help="Amount should be in VND",
                                 placeholder="50000")
        type_of_expense = st.pills("Type of Expense",
                                    options=option_map.keys(),
                                    format_func=lambda option: option_map[option],
                                    selection_mode="single",
                                    default=4
                                )
        notes = st.text_input("Notes",placeholder="Input note here...")
        st.write("Document Date:")
        left_insert,right_insert = st.columns([5,2])
        date = left_insert.date_input("Document Date",
                                      "today",
                                      format="DD/MM/YYYY",
                                      label_visibility="collapsed",
                                      max_value=datetime.today())
        submit_bttn = right_insert.button('Submit',
                                          use_container_width=True,
                                          icon=AppIcons.SAVE,
                                          type="primary")

        if type_of_expense is not None:
            pass
        else:
            raise ValueError(AppMessages.INVALID_EXPENSE_TYPE)

        if submit_bttn:
            initial_data[option_map[type_of_expense]] = amount
            initial_data["Date"] = date.strftime("%d/%m/%Y")
            initial_data["Note"] = notes
            df.loc[len(df)] = initial_data
            df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
            df = df.sort_values(by=['Date'])
            datasource.add_from(df)
            st.cache_data.clear()
            st.rerun()
    except ValueError as err:
        st.error(AppMessages.get_validation_errors(err.args),icon=AppIcons.ERROR)


header.add_header()

try:
    worksheet = datasource.get_detail_sheets()
except ConnectionError as err:
    st.error(AppMessages.get_connection_errors(err.args),icon=AppIcons.ERROR)
    
col1,col2,col3 = st.columns([3,1,1],vertical_alignment="bottom")
placeholder = st.empty()
expander = placeholder.expander("Expand for Data Grid",False)

today = datetime.now()
start_date = today.replace(day=1)
last_day = calendar.monthrange(today.year, today.month)[1]
end_date = today.replace(day=last_day)

selected_span = col1.date_input(
    "Select your expense span",
    (start_date, end_date),
    format="DD/MM/YYYY",
)


if col2.button("Sync",use_container_width=True, icon=AppIcons.SYNC,type="primary"):
    placeholder.empty()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()
    
insert_bttn =  col3.button("Insert",use_container_width=True, icon=AppIcons.INSERT_PAGE,type="primary")

if len(selected_span) < 2:
    st.warning(AppMessages.INVALID_DATE, icon=AppIcons.WARNING)
else: 
    data = datasource.filter(worksheet,selected_span)

    if insert_bttn:
        insert(worksheet)
    expander.dataframe(data,use_container_width=True,height=35*len(data)+38,hide_index=True)