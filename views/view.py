import streamlit as st
from datetime import datetime
import lib.common as common
import lib.headers as header

conn,worksheet_names = common.get_sheets()

header.add_header()

if 'sheet_key' not in st.session_state:
    st.session_state['sheet_key'] =datetime.today().strftime('%B-%Y')

if 'sheet' not in st.session_state:
    st.session_state['sheet'] = common.clean(conn.read(worksheet=st.session_state['sheet_key']))
    

col1,col2 = st.columns([5,2])

sheet = st.session_state['sheet']



with col1:
    option = st.selectbox(label="Sheet Select",
                        options = worksheet_names,
                        index=common.find_key(worksheet_names,st.session_state['sheet_key']),
                        label_visibility="collapsed"
                    )
    if option:
        sheet = common.clean(conn.read(worksheet=option))
        st.session_state['sheet'] = sheet
    

with col2:
    refresh_button = st.button("Refresh",use_container_width=True, icon=":material/sync:",type="primary")
    


st.dataframe(sheet,use_container_width=True,height=35*len(sheet)+38,hide_index=True)

if refresh_button: 
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()