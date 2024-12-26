import streamlit as st
from datetime import datetime
from classes.icons import AppIcons
from classes.messages import AppMessages
from classes.structure import DataStructure
import lib.datasource as datasource
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
    conn,worksheet_names = datasource.get_sheets()
    if 'sheet' not in st.session_state:
        st.session_state['sheet'] = datasource.clean(conn.read(worksheet=st.session_state['sheet_key']))
except ConnectionError as err:
    st.error(AppMessages.get_connecition_errors(err.args),icon=AppIcons.ERROR)

sheet = st.session_state['sheet']

col1,col2 = st.columns([3,2])
option = col1.selectbox(label="Sheet Select",
                    options = worksheet_names,
                    index=datasource.find_key(worksheet_names,st.session_state['sheet_key']),
                    label_visibility="collapsed"
                )
refresh_button = col2.button("Sync",use_container_width=True, icon=AppIcons.SYNC,type="primary")
placeholder = st.empty()


if option:
    sheet = datasource.read_from(conn,option)
    st.session_state['sheet'] = sheet
    
if len(sheet) >0:
    tab1,tab2,tab3 = placeholder.tabs(["Area :material/area_chart:", "Bar :material/insert_chart:", "Pie :material/pie_chart:"])
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
    st.warning(AppMessages.WARNING_CHANGES_NOT_SAVED,icon=AppIcons.ERROR)

if refresh_button:
    placeholder.empty()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()