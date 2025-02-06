""" Dashboard Page for the Visualization. """

from datetime import datetime, timedelta
from matplotlib.dates import relativedelta
import plotly.express as px
import streamlit as st
from millify import millify
from classes.icons import AppIcons
from classes.messages import AppMessages
from classes.structure import DataStructure
import lib.datasource as Datasource
import lib.utils as utils
import plotly.graph_objects as go
import pandas as pd 
import numpy as np
import calendar
app_lang = AppMessages(st.session_state.language)

@st.dialog(app_lang.INSERT_FORM)
def insert(df):
    """
        Create a insert dialog form
    """
    try:
        option_map, initial_data = Datasource.set_up_data()
        amount = st.number_input(app_lang.AMOUNT_TOOLTIP_NAME,min_value=0,
                                 step=1000,help=app_lang.AMOUNT_TOOLTIP,
                                 placeholder="50000")
        type_of_expense = st.pills(app_lang.TYPE_TOOLTIP_NAME,
                                    options=option_map.keys(),
                                    format_func=lambda option: option_map[option],
                                    selection_mode="single",
                                    default=0
                                )
        extra_type = st.empty()
        st.write(app_lang.DATEINPUT_TOOLTIP_NAME)
        left_insert,right_insert = st.columns(2)
        date = left_insert.date_input("Document Date",
                                      "today",
                                      format="DD/MM/YYYY",
                                      label_visibility="collapsed",
                                      max_value=utils.get_endtime_of_today())
        time = right_insert.time_input("Document Time",
                                      "now",
                                      label_visibility="collapsed")
        st.write(app_lang.NOTE_TOOLTIP_NAME)
        left_insert,right_insert = st.columns([5,2])
        notes = left_insert.text_input(app_lang.NOTE_TOOLTIP_NAME,placeholder=app_lang.NOTE_TOOLTIP,label_visibility='collapsed')
        submit_bttn = right_insert.button(app_lang.SAVE_BUTTON,
                                          use_container_width=True,
                                          icon=AppIcons.SAVE,
                                          type="primary")

        if type_of_expense is None:
            raise ValueError(app_lang.INVALID_EXPENSE_TYPE)
        elif type_of_expense == 4:
            expense_type = extra_type.text_input(app_lang.OTHER_TYPE_TOOLTIP_NAME,"Misc",20,placeholder="Misc")
        else:
            expense_type =  option_map[type_of_expense]
            
        if submit_bttn:
            initial_data["Type"] = expense_type
            initial_data["Spent"] = amount
            initial_data["Date"] = datetime.combine(date,time)
            initial_data["Note"] = notes
            df.loc[len(df)] = initial_data
            df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
            df = df.sort_values(by=['Date'])
            Datasource.update_from(df)
            st.cache_data.clear()
            st.rerun()
    except ValueError as err:
        st.error(app_lang.get_validation_errors(err.args),icon=AppIcons.ERROR)

@st.dialog(app_lang.UPDATE_FORM,width="large")
def update(sheet,selected_span):
    """ Update Dialog."""
    try:
        saved = False
        sheet["Type"] = sheet["Type"].astype(str)
        data_update, remaining = utils.filter(sheet,selected_span)
        update_placeholder = st.empty()
        tmp_df = st.data_editor(data_update,
                                use_container_width=True,
                                height=35*len(data_update)+36*2,
                                hide_index=True,
                                column_config=DataStructure.get_column_configs(),
                                num_rows='dynamic')
        
        
        
        if st.button(app_lang.SAVE_BUTTON, use_container_width=True, type="primary", icon=AppIcons.SAVE):
            # Add updated data_update back to sheet
            update = pd.concat([remaining, tmp_df], ignore_index=True)
            Datasource.update_from(update)
            saved = True
            st.cache_data.clear()
            st.rerun()
        if saved ==False:
            raise ValueError(app_lang.WARNING_CHANGES_NOT_SAVED)
    except ValueError as err:
        update_placeholder.warning(err.args[0],icon=AppIcons.ERROR)

@st.dialog(app_lang.EXPORT_FORM)
def export_form(sheet,selected_span):
    """ Export Dialog."""
    export_placeholder = st.empty()
    if len(sheet) > 0:
        left,right = st.columns([5,2],vertical_alignment="bottom")
        if st.toggle(app_lang.EXPORT_TOGGLE_TOOLTIP):
            dataframe_show = sheet
        else:
            dataframe_show,_ = utils.filter(sheet,selected_span)
        dataframe_show = pd.DataFrame(dataframe_show).sort_values("Date",ignore_index=True,ascending=False)
        
        file_type = left.segmented_control(app_lang.EXPORT_TYPE_TOOLTIP_NAME,
                               options=DataStructure.get_export_type().keys(),
                               format_func=lambda option: DataStructure.get_export_type()[option],
                               selection_mode="single",
                               default=0,
                               help=app_lang.EXPORT_TYPE_TOOLTIP)
        
        data_export, file_name = utils.get_export_data(dataframe_show,file_type)
        right.download_button(label=app_lang.EXPORT_BUTTON,
                           data=data_export,
                           file_name=file_name,
                           use_container_width=True,
                           type="primary",
                           icon=AppIcons.EXPORT_PAGE)
        st.expander(app_lang.EXPANDER).dataframe(dataframe_show,
                    use_container_width=True,
                    hide_index=True
                    )
    else:
        export_placeholder.warning(app_lang.WARNING_SHEET_EMPTY,icon=AppIcons.ERROR)

def plotly_pie_process(df):
    """ Return a pie plot the type of expensies distribution. """

    totals = df.groupby('Type')['Spent'].sum()
    total_sum = totals.sum()
    percentages = (totals / total_sum) * 100

    # Group categories with less than 5% into "Other"
    grouped_totals = totals[percentages >= 5]
    other_total = totals[percentages < 5].sum()

    if other_total > 0:
        grouped_totals['Other'] = other_total

    fig = px.pie(values=grouped_totals, names=grouped_totals.index, height=260)
    return fig

def plotly_calendar_process(df):
    """ Return dataframe total spent by day. """
    # Convert 'Date' to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    
    # Sum the spending across all categories
    df_daily = df.groupby('Date')['Spent'].sum().reset_index()
    df_daily.rename(columns={'Spent': 'Total_Spending'}, inplace=True)
    
    # Add columns for day of the week and week of the month
    df_daily['day'] = df_daily['Date'].dt.day
    df_daily['weekday'] = df_daily['Date'].dt.weekday
    df_daily['week'] = (df_daily['Date'].dt.day - 1) // 7

    # Generate a complete range for the month including the previous and next month days to fill the weeks
    start_date = df_daily['Date'].min() - pd.DateOffset(days=df_daily['Date'].min().weekday())
    end_date = df_daily['Date'].max() + pd.DateOffset(days=6 - df_daily['Date'].max().weekday())
    complete_dates = pd.date_range(start=start_date, end=end_date)

    # Create a DataFrame for the complete range
    complete_df = pd.DataFrame({'Date': complete_dates})
    complete_df['Total_Spending'] = 0  # Initialize with 0 spending

    # Merge with the actual spending data
    complete_df = pd.merge(complete_df, df_daily[['Date', 'Total_Spending']], on='Date', how='left', suffixes=('', '_actual'))
    complete_df['Total_Spending'] = complete_df['Total_Spending_actual'].combine_first(complete_df['Total_Spending'])

    # Add columns for day of the week and week of the month
    complete_df['day'] = complete_df['Date'].dt.day
    complete_df['weekday'] = complete_df['Date'].dt.weekday
    complete_df['week'] = ((complete_df['Date'] - start_date).dt.days) // 7

    # Create a matrix for the heatmap
    heatmap_data = np.zeros((complete_df['week'].max() + 1, 7))  # Number of weeks, 7 days
    for _, row in complete_df.iterrows():
        heatmap_data[row['week'], row['weekday']] = row['Total_Spending']

    custom_colorscale = [
        [0, '#ffffff'],
        [1, '#f54242']
    ]

    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=list(calendar.day_abbr),
        y=[f"{app_lang.WEEK_TOOLTIP} {i+1}" for i in range(heatmap_data.shape[0])],
        colorscale=custom_colorscale,
        colorbar=dict(title="Spending"),
    ))

    fig.update_layout(
        xaxis_title=app_lang.DAY_OF_WEEK_TOOLTIP,
        yaxis_title=app_lang.WEEK_OF_MONTH_TOOLTIP,
        height=260
    )

    return fig

today = datetime.now()
start_date = today.replace(day=1)
last_day = calendar.monthrange(today.year, today.month)[1]
end_date = today.replace(day=last_day)


col1,col2_2,col2_3,col3,col4,col5 = st.columns([1,4,4,1,1,2],vertical_alignment="bottom")

col1.image(utils.get_image(st.experimental_user.picture),use_container_width=True)


selected_month = col2_2.selectbox(app_lang.MONTH_TOOLTIP, range(1, 13),format_func= lambda option: f"{option:02d}",index=today.month-1)
selected_year = col2_3.selectbox(app_lang.YEAR_TOOLTIP, range(2024, today.year+1),index=today.year-2024)

refresh_button = col3.button(AppIcons.SYNC,use_container_width=True, type="primary")

insert_bttn =  col4.button(AppIcons.INSERT_PAGE,use_container_width=True, type="primary")


with col5.popover(AppIcons.MENU_PAGE,use_container_width=True):
    utils.add_change_lang()
    update_bttn =  st.button(app_lang.UPDATE_BUTTON,use_container_width=True, icon=AppIcons.MANAGE_PAGE,type="secondary")
    export_bttn =  st.button(app_lang.EXPORT_BUTTON,use_container_width=True, icon=AppIcons.EXPORT_PAGE,type="secondary")
    st.button(app_lang.LOGOUT_BUTTON,use_container_width=True, icon=AppIcons.LOG_OUT,type="secondary",on_click=utils.sign_out)

metrics,calendar_chart,line_chart,bar_plot,pie_plot,dataframe_tab = st.tabs(
    [f"{AppIcons.METRICS} {app_lang.METRICS}",
    f"{AppIcons.HEAT_MAP} {app_lang.HEAT_MAP}",
    f"{AppIcons.LINE_CHART} {app_lang.LINE_CHART}",
    f"{AppIcons.BAR_CHART} {app_lang.BAR_CHART}",
    f"{AppIcons.PIE_CHART} {app_lang.PIE_CHART}",
    f"{AppIcons.DATA_FRAME} {app_lang.DATA_FRAME}"]
)

try:
    sheet = Datasource.get_detail_sheets()
except ConnectionError as err:
    st.error(app_lang.get_connection_errors(err.args),icon=AppIcons.ERROR)

start_date,end_date = utils.get_start_and_end(datetime.strptime(f"01/{selected_month}/{selected_year}","%d/%m/%Y"))

with st.spinner(app_lang.LOADING_TOOLTIP):
    data,_ = utils.filter(sheet,(start_date.date(),end_date.date()))
    if insert_bttn:
        insert(sheet)
    if update_bttn:
        update(sheet,(start_date.date(),end_date.date()))
    if export_bttn:
        export_form(sheet,(start_date.date(),end_date.date()))
    if len(data) >0:
        
        with metrics:
            m_l,m_m,m_r = st.columns([1,1,1],vertical_alignment='top')
            m_l.header("Compare with ",anchor=False)
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
            plotly_calendar_process(plotly),
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
        
        pie_plot.plotly_chart(plotly_pie_process(data),use_container_width=True)
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
