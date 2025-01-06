""" Dashboard Page for the Visualization. """

from datetime import datetime
import plotly.express as px
import streamlit as st
from millify import millify
from classes.icons import AppIcons
from classes.messages import AppMessages
from classes.structure import DataStructure
import lib.datasource as Datasource
import lib.headers as header
import plotly.graph_objects as go
import pandas as pd 
import numpy as np
import calendar

@st.dialog("Insert Data")
def insert(df):
    """
        Create a insert dialog form
    """
    try:
        option_map, initial_data = Datasource.set_up_data()
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
            Datasource.add_from(df)
            st.cache_data.clear()
            st.rerun()
    except ValueError as err:
        st.error(AppMessages.get_validation_errors(err.args),icon=AppIcons.ERROR)

def not_saved():
    """ Show warning when not saved. """
    st.error(AppMessages.WARNING_CHANGES_NOT_SAVED, icon=AppIcons.WARNING)

@st.dialog("Edit Data",width="large")
def update(sheet,selected_span):
    """ Update Dialog."""
    data_update = Datasource.filter(sheet,selected_span)
    placeholder = st.empty()
    tmp_df = st.data_editor(data_update,
                            use_container_width=True,
                            height=35*len(data_update)+36*2,
                            hide_index=True,
                            column_config=DataStructure.get_column_configs(),
                            on_change=not_saved,
                            num_rows='dynamic')
    if st.button("Save",use_container_width=True,type="primary",icon=AppIcons.SAVE):
        Datasource.update_from(tmp_df,data_update,sheet)
        st.cache_data.clear()
        st.rerun()

def plotly_pie_process(df):
    """ Return a pie plot the type of expensies distribution. """
    categories = DataStructure.get_categories_numeric()
    totals = df[categories].sum()
    total_sum = totals.sum()
    percentages = (totals / total_sum) * 100

    # Group categories with less than 5% into "Other"
    grouped_totals = totals[percentages >= 5]
    other_total = totals[percentages < 5].sum()

    if other_total > 0:
        grouped_totals['Other'] = other_total

    fig = px.pie(values=grouped_totals, names=grouped_totals.index, height=260)
    return fig

def normal_plot_data(df):
    """ Return group by date, category. """
    # Add columns for year, month, day, and week
    df = df.drop(['Note'], axis=1)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    # Sum the total spending by day
    return df.groupby('Date')[DataStructure.get_categories_numeric()].sum().reset_index()

def plotly_calendar_process(df):
    """ Return dataframe total spent by day. """
    # Add columns for year, month, day, and week
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    # Sum the spending across all categories
    df['Total_Spending'] = df[DataStructure.get_categories_numeric()].sum(axis=1)
    # Add columns for day of the week and week of the month
    
    # Sum the total spending by day
    df_daily = df.groupby('Date')['Total_Spending'].sum().reset_index()
    
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
        y=[f"Week {i+1}" for i in range(heatmap_data.shape[0])],
        colorscale=custom_colorscale,
        colorbar=dict(title="Spending"),
    ))

    fig.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Week of Month",height=260
    )

    return fig

header.add_header()

try:
    sheet = Datasource.get_detail_sheets()
except ConnectionError as err:
    st.error(AppMessages.get_connection_errors(err.args),icon=AppIcons.ERROR)

col1,col2,col3,col4 = st.columns([3,1,2,2],vertical_alignment="bottom")

today = datetime.now()
start_date = today.replace(day=1)
last_day = calendar.monthrange(today.year, today.month)[1]
end_date = today.replace(day=last_day)

if sheet is not None and len(sheet) >0:
    oldest_record = pd.to_datetime(sheet['Date'],format="%d/%m/%Y").min().date()
else:
    oldest_record = start_date.date()

selected_span = col1.date_input(
    "Select your expense span",
    (start_date, end_date),
    format="DD/MM/YYYY",
    min_value=oldest_record,
    help="The oldest date is: " + oldest_record.strftime("%d/%m/%Y")
    
)

refresh_button = col2.button(AppIcons.SYNC,use_container_width=True, type="primary")
insert_bttn =  col3.button("Insert",use_container_width=True, icon=AppIcons.INSERT_PAGE,type="primary")
update_bttn =  col4.button("Edit",use_container_width=True, icon=AppIcons.MANAGE_PAGE,type="primary")
placeholder = st.empty()


if len(selected_span) < 2 or selected_span[0] < oldest_record:
    st.warning(AppMessages.INVALID_DATE, icon=AppIcons.WARNING)
else: 
    data = Datasource.filter(sheet,selected_span)
    if insert_bttn:
        insert(sheet)
    if update_bttn:
        update(sheet,selected_span)
    if len(data) >0:
        
        metrics_src = Datasource.get_metrics(sheet,start_date,end_date)
        
        metrics,calendar_chart,line_chart,bar_plot,pie_plot,dataframe_tab = placeholder.tabs(
            [AppIcons.METRICS+" Metrics",
            AppIcons.HEAT_MAP+ " Spending Map",
            AppIcons.LINE_CHART+" Line",
            AppIcons.BAR_CHART+" Bar",
            AppIcons.PIE_CHART+" Pie",
            AppIcons.DATA_FRAME+" Data"])
        metrics.write("Current month metrics compare to last month.")
        spending,max_spent,largest_cate = metrics.columns(3)
        total_spent, highest_single, highest_category, highest_category_value   = Datasource.get_delta(metrics_src, sheet)
        
        spending.metric("Total Spending (VND)",
                        millify(metrics_src["Total"],precision=3),
                        delta=millify(total_spent,precision=3),
                        delta_color="inverse",
                        help=None,
                        label_visibility="visible",
                        border=True)

        max_spent.metric("Highest Spending (VND)",
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
                            help="Old: "+highest_category,
                            label_visibility="visible",
                            border=True)
        calendar_chart.plotly_chart(
            plotly_calendar_process(Datasource.filter(sheet,selected_span)),use_container_width=True
        )

        normal_data = normal_plot_data(data)
        line_chart.line_chart(
            normal_data,
            x="Date",
            y=DataStructure.get_categories_numeric(),
            use_container_width= True,
            height=250
        )

        bar_plot.bar_chart(
            normal_data,
            x="Date",
            y=DataStructure.get_categories_numeric(),
            use_container_width= True,
            stack=True,
            height=250
        )
        
        pie_plot.plotly_chart(plotly_pie_process(data),use_container_width=True)
        dataframe_tab.dataframe(data,
                                use_container_width=True,
                                height=35*len(data)+36*2,
                                hide_index=True,
                                column_config=DataStructure.get_column_configs())
    else:
        st.warning(AppMessages.WARNING_SHEET_EMPTY,icon=AppIcons.ERROR)

    if refresh_button:
        placeholder.empty()
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
