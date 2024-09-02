import pandas as pd
import plotly.express as px


def bar_device_usage(combined_df2):
    # Convert 'Start_Date' column to datetime objects
    combined_df2['Start_Date'] = pd.to_datetime(combined_df2['Start_Date'])
    combined_df2['End_Date'] = pd.to_datetime(combined_df2['End_Date'])

    # Convert duration columns to numeric values, ignoring errors
    combined_df2['Average Active Duration(Minutes)'] = pd.to_numeric(
        combined_df2['Average Active Duration(Minutes)'], errors='coerce')
    combined_df2['Average Idle Duration(Minutes)'] = pd.to_numeric(
        combined_df2['Average Idle Duration(Minutes)'], errors='coerce')

    # Filter the DataFrame to include only the last 7 days
    last_7_days_df = combined_df2.loc[
        combined_df2['Start_Date'] >= combined_df2['Start_Date'].max() - pd.Timedelta(days=6)].copy()

    # Fill NaN values with 0
    last_7_days_df['Average Active Duration(Minutes)'].fillna(0, inplace=True)
    last_7_days_df['Average Idle Duration(Minutes)'].fillna(0, inplace=True)

    # Calculate total duration by summing Device Active Duration and Device Idle Duration
    last_7_days_df['Average Total Duration (Minutes)'] = (
            last_7_days_df['Average Active Duration(Minutes)'] + last_7_days_df['Average Idle Duration(Minutes)'])

    # Convert duration columns to hours
    last_7_days_df['Average Active Duration(Hours)'] = last_7_days_df['Average Active Duration(Minutes)'] / 60
    last_7_days_df['Average Idle Duration(Hours)'] = last_7_days_df['Average Idle Duration(Minutes)'] / 60
    last_7_days_df['Average Total Duration (Hours)'] = last_7_days_df['Average Total Duration (Minutes)'] / 60

    # Melt the DataFrame
    melted_df = pd.melt(last_7_days_df, id_vars=['Start_Date'],
                        value_vars=['Average Active Duration(Hours)', 'Average Idle Duration(Hours)'],
                        var_name='Type', value_name='Duration (Hours)')

    # Plot a bar chart using Plotly
    fig = px.bar(melted_df, x='Start_Date', y='Duration (Hours)', color='Type',
                 color_discrete_map={'Average Active Duration(Hours)': 'blue',
                                     'Average Idle Duration(Hours)': 'orange'},
                 labels={'Duration (Minutes)': 'Duration (Minutes)', 'Start_Date': 'Date'},
                 title='Device Usage per Day (Last 7 Days)')

    fig.update_layout(xaxis_tickangle=-45)

    return fig
