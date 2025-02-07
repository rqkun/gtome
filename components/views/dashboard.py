""" Dashboard Page for the Visualization. """

from datetime import datetime, timedelta
from matplotlib.dates import relativedelta
import plotly.express as px
import streamlit as st
from millify import millify
from configs.icons import AppIcons
from configs.messages import AppMessages
from configs.structure import DataStructure
from components import plots
import components.custom_components
import configs.datasource as Datasource
import configs.utils as utils
from components.dialogs import insert_dialog,update_dialog,export_dialog

app_lang = AppMessages(st.session_state.language)

@st.dialog(app_lang.INSERT_FORM)
def insert(df):
    insert_dialog.show(df)

@st.dialog(app_lang.UPDATE_FORM,width="large")
def update(sheet,selected_span):
    update_dialog.show(sheet,selected_span)

@st.dialog(app_lang.EXPORT_FORM)
def export(sheet,selected_span):
    export_dialog.show(sheet,selected_span)

try:
    sheet = Datasource.get_detail_sheets()
except ConnectionError as err:
    st.error(app_lang.get_connection_errors(err.args),icon=AppIcons.ERROR)

with st.spinner(app_lang.LOADING_TOOLTIP, show_time=True):
    
    today, latest_date = utils.get_inital_date_values(sheet)
    
    col1,col2_2,col2_3,col3,col4,col5 = st.columns([1,4,4,1,1,2],vertical_alignment="bottom")

    col1.image(utils.get_image(st.experimental_user.picture),use_container_width=True)
    selected_month = col2_2.selectbox(app_lang.MONTH_TOOLTIP, range(1, 13),format_func= lambda option: f"{option:02d}",index=latest_date.month-1)
    selected_year = col2_3.selectbox(app_lang.YEAR_TOOLTIP, range(2024, today.year+1),index=latest_date.year-2024)
    refresh_button = col3.button(AppIcons.SYNC,use_container_width=True, type="primary")
    insert_bttn =  col4.button(AppIcons.INSERT_PAGE,use_container_width=True, type="primary")

    with col5.popover(AppIcons.MENU_PAGE,use_container_width=True):
        components.custom_components.change_language_button()
        update_bttn =  st.button(app_lang.UPDATE_BUTTON,use_container_width=True, icon=AppIcons.MANAGE_PAGE,type="secondary")
        export_bttn =  st.button(app_lang.EXPORT_BUTTON,use_container_width=True, icon=AppIcons.EXPORT_PAGE,type="secondary")
        st.link_button("Github","https://github.com/rqkun/gtome",icon=AppIcons.BUG_REPORT_PAGE,use_container_width=True)
        st.button(app_lang.LOGOUT_BUTTON,use_container_width=True, icon=AppIcons.LOG_OUT,type="secondary",on_click=components.custom_components.sign_out_callable)
    
    metrics,calendar_chart,line_chart,bar_plot,pie_plot,dataframe_tab = st.tabs(
        [f"{AppIcons.METRICS} {app_lang.METRICS}",
        f"{AppIcons.HEAT_MAP} {app_lang.HEAT_MAP}",
        f"{AppIcons.LINE_CHART} {app_lang.LINE_CHART}",
        f"{AppIcons.BAR_CHART} {app_lang.BAR_CHART}",
        f"{AppIcons.PIE_CHART} {app_lang.PIE_CHART}",
        f"{AppIcons.DATA_FRAME} {app_lang.DATA_FRAME}"]
    )

start_date,end_date = utils.get_start_and_end(datetime.strptime(f"01/{selected_month}/{selected_year}","%d/%m/%Y"))

with st.spinner(app_lang.LOADING_TOOLTIP):
    data,_ = utils.filter(sheet,(start_date.date(),end_date.date()))
    if insert_bttn:
        insert(sheet)
    if update_bttn:
        update(sheet,(start_date.date(),end_date.date()))
    if export_bttn:
        export(sheet,(start_date.date(),end_date.date()))
    if len(data) >0:
        
        with metrics:
            m_l,m_m,m_r = st.columns([1,1,1],vertical_alignment='top')
            m_l.header(app_lang.COMPARING_TOOLTIP,anchor=False)
            lastmonth = start_date - relativedelta(months=1)
            compared_month = m_m.selectbox(app_lang.MONTH_TOOLTIP, range(1, 13),format_func= lambda option: f"{option:02d}",index=lastmonth.month-1,key='compared_month')
            compared_year = m_r.selectbox(app_lang.YEAR_TOOLTIP, range(2024, today.year+1),index=lastmonth.year-2024,key='compared_year')
            last_start_date,last_end_date = utils.get_start_and_end(datetime.strptime(f"01/{compared_month}/{compared_year}","%d/%m/%Y"))

        metrics_src = utils.get_metrics(sheet,start_date,end_date)
        spending,max_spent,largest_cate = metrics.columns(3)
        total_spent, highest_single, highest_category, highest_category_value   = utils.get_delta(metrics_src, sheet, (last_start_date,last_end_date))
        
        spending.metric(app_lang.TOTAL_SPENDING_TOOLTIP,
                        millify(metrics_src["Total"],precision=3),
                        delta=millify(total_spent,precision=3),
                        delta_color="inverse",
                        help=None,
                        label_visibility="visible",
                        border=True)

        max_spent.metric(app_lang.HIGHEST_SPENDING_TOOLTIP,
                        millify(metrics_src["Highest"],precision=3),
                        delta=millify(highest_single,precision=3),
                        delta_color="inverse",
                        help=None,
                        label_visibility="visible",
                        border=True)

        largest_cate.metric(metrics_src["Highest_Category"] +" (VND)",
                            millify(metrics_src["Highest_Category_Value"],precision=3),
                            delta=millify(highest_category_value,precision=3),
                            delta_color="inverse",
                            help=f"{app_lang.OLD_METRIC_TOOLTIP}: {highest_category}",
                            label_visibility="visible",
                            border=True)
        
        plotly,_  = utils.filter(sheet,(start_date.date(),end_date.date()))
        calendar_chart.plotly_chart(
            plots.plotly_calendar(plotly),
            use_container_width=True
        )

        normal_data = utils.normal_plot_data(data)
        line_chart.line_chart(
            data=normal_data.pivot(index='Date', columns='Type', values='Spent').fillna(0),
            use_container_width=True,
            height=250
        )

        bar_plot.bar_chart(
            data=normal_data.pivot(index='Date', columns='Type', values='Spent').fillna(0),
            use_container_width=True,
            height=250,
            stack=True,
        )
        
        pie_plot.plotly_chart(plots.plotly_pie(data),use_container_width=True)
        
        dataframe_tab.dataframe(data.sort_values(by=['Date'],ascending=False),
                                use_container_width=True,
                                height=35*len(data)+36*2,
                                hide_index=True,
                                column_config=DataStructure.get_column_configs())
    else:
        st.warning(app_lang.WARNING_SHEET_EMPTY,icon=AppIcons.ERROR)

    if refresh_button:
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
