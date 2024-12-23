import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd

@st.cache_resource  
def connect_to_gsheet():
    return st.connection("gsheets", type=GSheetsConnection)

# @st.cache_data
# def store_df(data):
#     if 'data' not in st.session_state:
#         st.session_state['data'] = data
#     return data


def filter_data(input):
    df = conn.read(worksheet=input)
    df[["Food","Rent","Traverse","Subscriptions","Misc","Fun"]] = df[["Food","Rent","Traverse","Subscriptions","Misc","Fun"]].fillna(0)
    df = df.drop(columns=["Note"])
    rows, _ = df.shape
    st.dataframe(df,use_container_width=True,height=rows*36)

def find_key(list_str,value):
    try:
        return list_str.index(value)
    except:
        return len(list_str)-1

def create_if_none_latest():
    today = datetime.today().strftime('%B-%Y')
    temp_df = pd.DataFrame(columns=['Date','Food','Rent','Traverse','Subscriptions','Misc','Fun','Note'])
    if worksheet_names.count(today) ==0:
        conn.create(
            worksheet=today,
            data=temp_df,
        )
        st.rerun()
    
conn = connect_to_gsheet()

if 'sheet_key' not in st.session_state:
    st.session_state['sheet_key'] = datetime.today().strftime('%B-%Y')
    

worksheet_names = []
for sheet in conn.client._open_spreadsheet():
   worksheet_names.append(sheet.title)

create_if_none_latest()

option = st.selectbox(label="Sheet Select",
                        options = worksheet_names,
                        index=find_key(worksheet_names,st.session_state['sheet_key']),
                        label_visibility="collapsed"
                    )

st.session_state['sheet_key'] = option

filter_data(st.session_state['sheet_key'])


