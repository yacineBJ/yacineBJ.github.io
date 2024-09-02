import plotly.graph_objs as go


def plot_line_chart(combined_df):

    # Extract unique days from the 'Date (UTC)' column
    unique_days = combined_df['Date (UTC)'].unique()

    traces = []
    for day in unique_days:
        # Filter data for the selected day
        day_data = combined_df[combined_df['Date (UTC)'] == day]

        # Create a line trace
        trace = go.Scatter(x=day_data['Time'], y=day_data['Battery (%)'], mode='lines', name=f'Battery {day}')
        traces.append(trace)

    # Create layout for the plot
    layout = go.Layout(title='Line Chart for Battery History', xaxis_title='Time (UTC)', yaxis_title='Battery (%)')

    # Create figure and plot
    fig = go.Figure(data=traces, layout=layout)
    return fig