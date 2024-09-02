import pandas as pd
import plotly.express as px
from datetime import datetime, time


def bar_charging(combined_df):
    # Convert 'Date' column to datetime objects
    combined_df['Date (UTC)'] = pd.to_datetime(combined_df['Date (UTC)'], format='%d-%b-%Y')

    # Parse time strings into datetime.time objects
    combined_df['Time'] = combined_df['Time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time())

    # Filter the DataFrame to include only the last 7 days
    last_7_days_df = combined_df.loc[
        combined_df['Date (UTC)'] >= combined_df['Date (UTC)'].max() - pd.Timedelta(days=6)]

    # Step 3: Calculate charging and discharging durations for each day
    charge_times = []
    discharge_times = []

    for date, group in last_7_days_df.groupby('Date (UTC)',):
        charging = False
        start_time = None

        for _, row in group.iterrows():
            if row['Charging'] and not charging:
                start_time = row['Time']
                charging = True
            elif not row['Charging'] and charging:
                if start_time:
                    end_time = row['Time']
                    duration = (datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(),
                                                                                                start_time)).total_seconds() / 3600  # Convert to hours
                    if duration > 0:
                        charge_times.append((date, duration))
                charging = False

        # Check if charging was ongoing until the end of the day
        if charging and start_time:
            end_time = time(23, 59, 59)
            duration = (datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(),
                                                                                        start_time)).total_seconds() / 3600  # Convert to hours
            charge_times.append((date, duration))

        # Calculate discharging time
        discharge_time = 24 - sum([time[1] for time in charge_times if time[0] == date])
        discharge_times.append((date, discharge_time))

    # Combine charging and discharging data
    charge_df = pd.DataFrame(charge_times, columns=['Date (UTC)', 'Duration'])
    discharge_df = pd.DataFrame(discharge_times, columns=['Date (UTC)', 'Duration'])
    charge_df['Type'] = 'Charging'
    discharge_df['Type'] = 'Discharging'
    plot_df = pd.concat([charge_df, discharge_df])
    # Plot a bar chart using Plotly
    fig = px.bar(plot_df, x='Date (UTC)', y='Duration', color='Type',
                 labels={'Duration': 'Duration (hours)', 'Date (UTC)': 'Date (UTC)'},
                 title='Battery Charging and Discharging per Day (Last 7 Days)',
                 barmode='stack')
    fig.update_layout(xaxis_tickangle=-45)
    return fig
