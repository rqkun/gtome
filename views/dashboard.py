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

def plotly_calendar_process(df):
    """ Return a pie plot the type of expensies distribution. """
    # Add columns for year, month, day, and week
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    # Sum the spending across all categories
    df['Total_Spending'] = df[['Food', 'Rent', 'Traverse', 'Subscriptions', 'Misc', 'Fun']].sum(axis=1)
    # Add columns for day of the week and week of the month
    df['day'] = df['Date'].dt.day
    df['weekday'] = df['Date'].dt.weekday
    df['week'] = (df['Date'].dt.day - 1) // 7

    # Generate a complete range for the month including the previous and next month days to fill the weeks
    start_date = df['Date'].min() - pd.DateOffset(days=df['Date'].min().weekday())
    end_date = df['Date'].max() + pd.DateOffset(days=6 - df['Date'].max().weekday())
    complete_dates = pd.date_range(start=start_date, end=end_date)

    # Create a DataFrame for the complete range
    complete_df = pd.DataFrame({'Date': complete_dates})
    complete_df['Total_Spending'] = 0  # Initialize with 0 spending

    # Merge with the actual spending data
    complete_df = pd.merge(complete_df, df[['Date', 'Total_Spending']], on='Date', how='left', suffixes=('', '_actual'))
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

col1,col2 = st.columns([3,2],vertical_alignment="bottom")

today = datetime.now()
start_date = today.replace(day=1)
last_day = calendar.monthrange(today.year, today.month)[1]
end_date = today.replace(day=last_day)
if len(sheet) >0:
    oldest_record = pd.to_datetime(sheet['Date'],format="%d/%m/%Y").min().date()
else:
    oldest_record = today.date()
selected_span = col1.date_input(
    "Select your expense span",
    (start_date, end_date),
    format="DD/MM/YYYY",
    min_value=oldest_record,
    help="The oldest date is: " + oldest_record.strftime("%d/%m/%Y")
    
)

refresh_button = col2.button("Sync",use_container_width=True, icon=AppIcons.SYNC,type="primary")
placeholder = st.empty()


if len(selected_span) < 2:
    st.warning("Please choose a start/end date.", icon=AppIcons.WARNING)
elif selected_span[0] < oldest_record:
    st.warning("Please choose a valid date.", icon=AppIcons.WARNING)
else: 
    data = Datasource.filter(sheet,selected_span)
    if len(data) >0:
        
        metrics_src = Datasource.get_metrics(sheet,start_date,end_date)
        
        metrics,calendar_chart,line_chart,bar_plot,pie_plot = placeholder.tabs(
            [AppIcons.METRICS+" Metrics",
            AppIcons.HEAT_MAP+ " Spending Map",
            AppIcons.LINE_CHART+" Line",
            AppIcons.BAR_CHART+" Bar",
            AppIcons.PIE_CHART+" Pie"])
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
                            help=None,
                            label_visibility="visible",
                            border=True)
        calendar_chart.plotly_chart(
            plotly_calendar_process(data),use_container_width=True
        )
        
        line_chart.line_chart(
            data,
            x="Date",
            y=DataStructure.get_categories_numeric(),
            use_container_width= True,
            height=250
        )

        bar_plot.bar_chart(
            data,
            x="Date",
            y=DataStructure.get_categories_numeric(),
            use_container_width= True,
            stack=True,
            height=250
        )
        
        pie_plot.plotly_chart(plotly_pie_process(data),use_container_width=True)

    else:
        st.warning(AppMessages.WARNING_SHEET_EMPTY,icon=AppIcons.ERROR)

    if refresh_button:
        placeholder.empty()
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
