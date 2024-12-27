import streamlit as st
from datetime import datetime
from classes.icons import AppIcons
from classes.messages import AppMessages
from classes.structure import DataStructure
import lib.datasource as datasource
import lib.headers as header
import plotly.express as px
from millify import millify

def plotly_process(df):
    categories = DataStructure.get_categories_numeric()
    totals = df[categories].sum()
    total_sum = totals.sum()
    percentages = (totals / total_sum) * 100

    # Group categories with less than 5% into "Other"
    grouped_totals = totals[percentages >= 2]
    other_total = totals[percentages < 2].sum()

    if other_total > 0:
        grouped_totals['Other'] = other_total
        
    fig = px.pie(values=grouped_totals, names=grouped_totals.index)
    return fig

def calc_sum(df):
    categories = DataStructure.get_categories_numeric()
    totals = df[categories].sum()
    return millify(totals.sum(),precision=3)

def calc_max_spending(df):
    categories = DataStructure.get_categories_numeric()
    tmp = df[categories].max()
    return millify(tmp.max(),precision=3)

def calc_highest_sum(df):
    categories = DataStructure.get_categories_numeric()
    totals = df[categories].sum()
    return millify(totals.max(),precision=3), totals.idxmax()

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
    
    metrics,area_chart,bar_plot,pie_plot = placeholder.tabs(["Metrics :material/monitoring:","Area :material/area_chart:", "Bar :material/insert_chart:", "Pie :material/pie_chart:"])
    spending,max_spent,largest_cate = metrics.columns(3)
    spending.metric("Total Spending",calc_sum(sheet) +" VND", delta=0, delta_color="normal", help=None, label_visibility="visible", border=True)
    max_spent.metric("Highest Spending",calc_max_spending(sheet) +" VND", delta=0, delta_color="normal", help=None, label_visibility="visible", border=True)
    category_sum, category = calc_highest_sum(sheet)
    largest_cate.metric(category, category_sum+" VND", delta=0, delta_color="normal", help=None, label_visibility="visible", border=True)
    
    
    area_chart.area_chart(
        sheet,
        x="Date",
        y=DataStructure.get_categories_numeric(),
        use_container_width= True
    )
    bar_plot.bar_chart(
        sheet,
        x="Date",
        y=DataStructure.get_categories_numeric(),
        use_container_width= True
    )
    pie_plot.plotly_chart(plotly_process(sheet),use_container_width=True)
    
else: 
    st.warning(AppMessages.WARNING_SHEET_EMPTY,icon=AppIcons.ERROR)

if refresh_button:
    placeholder.empty()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()