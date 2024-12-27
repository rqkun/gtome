import streamlit as st
from datetime import datetime
import lib.datasource as datasource
import lib.headers as header
import pandas as pd
from classes.messages import AppMessages
from classes.icons import AppIcons
@st.dialog("Insert Data")
def insert(conn,df,option):
    try:
        option_map, initial_data = datasource.set_up_data()
        amount = st.number_input("Amount",min_value=0,step=1000,help="Amount should be in VND",placeholder="50000")
        type_of_expense = st.pills("Type of Expense",
                                    options=option_map.keys(),
                                    format_func=lambda option: option_map[option],
                                    selection_mode="single",
                                    default=4
                                )
        notes = st.text_input("Notes",placeholder="Input note here...")
        st.write("Document Date:")
        col1,col2 = st.columns([5,2])
        with col1:
            date = st.date_input("Document Date", "today", format="DD/MM/YYYY",label_visibility="collapsed",
                                min_value=datetime.strptime("1-"+option,'%d-%B-%Y'),
                                max_value=datetime.today())
        with col2:
            submit_bttn = st.button('Submit',use_container_width=True,icon=AppIcons.SAVE,type="primary")
        
        if type_of_expense:
            pass
        else:
            raise ValueError(AppMessages.VALIDATION_EXPENSE_TYPE,AppMessages.VALIDATION_ERROR_MISSING)
        if datetime.strptime(date.strftime("%d/%m/%Y"),"%d/%m/%Y")  > datetime.strptime("1-"+option,'%d-%B-%Y'):
            pass
        else:
            raise ValueError(AppMessages.VALIDATION_DATE,AppMessages.VALIDATION_ERROR_OOB)
        
        if submit_bttn:
            initial_data[option_map[type_of_expense]] = amount
            initial_data["Date"] = date.strftime("%d/%m/%Y")
            initial_data["Note"] = notes
            df.loc[len(df)] = initial_data
            df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
            df = df.sort_values(by=['Date'])
            datasource.update_from(conn,option,df)
            st.cache_data.clear()
            st.rerun()
    except ValueError as err:
        st.error(AppMessages.get_validation_errors(err.args),icon=AppIcons.ERROR)
        
header.add_header()



if 'sheet_key' not in st.session_state:
    st.session_state['sheet_key'] =datetime.today().strftime('%B-%Y')
try:
    conn,worksheet_names = datasource.get_sheets()
    if 'sheet' not in st.session_state:
        st.session_state['sheet'] = datasource.clean(conn.read(worksheet=st.session_state['sheet_key']))
except ConnectionError as err:
    st.error(AppMessages.get_connecition_errors(err.args),icon=AppIcons.ERROR)

sheet = st.session_state['sheet']

col1,col2,col3 = st.columns([3,1,1])
placeholder = st.empty()
option = col1.selectbox(label="Sheet Select",
                    options = worksheet_names,
                    index=datasource.find_key(worksheet_names,st.session_state['sheet_key']),
                    label_visibility="collapsed"
                )

if col2.button("Sync",use_container_width=True, icon=AppIcons.SYNC,type="primary"): 
    placeholder.empty()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()
if col3.button("Insert",use_container_width=True, icon=AppIcons.INSERT_PAGE,type="primary"): 
    insert(conn,sheet,option)
if option:
    sheet = datasource.read_from(conn,option)
    st.session_state['sheet'] = sheet

placeholder.dataframe(sheet,use_container_width=True,height=35*len(sheet)+38,hide_index=True) 






