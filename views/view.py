import streamlit as st
from datetime import datetime
from classes.messages import MessageConstants
from classes.structure import DataStructure
import lib.common as common
import lib.headers as header
import plotly.express as px

def plotly_process(df):
    categories = DataStructure.get_categories_numeric()
    totals = df[categories].sum()
    fig = px.pie(values=totals, names=categories)
    return fig


header.add_header()

if 'sheet_key' not in st.session_state:
    st.session_state['sheet_key'] =datetime.today().strftime('%B-%Y')
try:
    conn,worksheet_names = common.get_sheets()
    if 'sheet' not in st.session_state:
        st.session_state['sheet'] = common.clean(conn.read(worksheet=st.session_state['sheet_key']))
except ConnectionError as err:
    st.error(MessageConstants.get_connecition_errors(err.args),icon=":material/error:")

sheet = st.session_state['sheet']

col1,col2 = st.columns([5,1])
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
    refresh_button = st.button("Sync",use_container_width=True, icon=":material/sync:",type="primary")

if len(sheet) >0:
    tab1,tab2,tab3 = st.tabs(["Area :material/area_chart:", "Bar :material/insert_chart:", "Pie :material/pie_chart:"])
    tab1.area_chart(
        sheet,
        x="Date",
        y=DataStructure.get_categories_numeric(),
        use_container_width= True
    )
    tab2.bar_chart(
        sheet,
        x="Date",
        y=DataStructure.get_categories_numeric(),
        use_container_width= True
    )
    tab3.plotly_chart(plotly_process(sheet),use_container_width=True)
    
else: 
    st.warning("Sheet currently empty.",icon=":material/error:")

if refresh_button: 
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()