import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

@st.cache_resource  
def connect_to_gsheet():
    return st.connection("gsheets", type=GSheetsConnection)

conn = connect_to_gsheet()

if 'sheet_key' not in st.session_state:
    st.session_state['sheet_key'] = datetime.today().strftime('%B-%Y')
    
    
def filter_data(input):
    df = conn.read(worksheet=input)
    df = df.drop(0)
    df[["Food","Rent","Traverse","Subscriptions ","Misc","Fun"]] = df[["Food","Rent","Traverse","Subscriptions ","Misc","Fun"]].fillna(0)
    df = df.drop(columns=["Note"])
    rows, columns = df.shape
    st.dataframe(df,use_container_width=True,height=rows*36)

def find_key(list_str,value):
    try:
        return list_str.index(value)
    except:
        return len(list_str)-1



worksheet_names = []
for sheet in conn.client._open_spreadsheet():
   worksheet_names.append(sheet.title)




option = st.selectbox(label="Sheet Select",
                        options = worksheet_names,
                        index=find_key(worksheet_names,st.session_state['sheet_key']),
                        label_visibility="collapsed"
                    )
st.session_state['sheet_key'] = option



filter_data(st.session_state['sheet_key'])
