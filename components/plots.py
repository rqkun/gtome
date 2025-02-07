import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 
import numpy as np
import calendar
import streamlit as st
from configs.messages import AppMessages
def plotly_pie(df):
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

def plotly_calendar(df):
    """ Return dataframe total spent by day. """
    app_lang = AppMessages(st.session_state.language)
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