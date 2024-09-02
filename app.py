import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

from ML_dashboard import (ML_plot)
from ML import Machine_Learning
# from API.ScalefusionAPI import device
from Cleaning_data import clean_data, clean_device_usage, clean_data2
from BatteryUsage import plot_line_chart
from BatteryStatus import bar_charging
from IDLE_Usage import bar_device_usage
from Cleaning_ML import cleaning_ML

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[
    "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css",
    "https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
])

# Call the clean_data function to get combined_df
cleaned_data = clean_data()

# Call the clean_device_usage function to get combined_df2
cleaned_data2 = clean_device_usage()

# Call the clean_data2 function to get filtered_data
cleaned_data3 = clean_data2(cleaned_data)

# Call the cleaning_ML function to get df
cleaning_ML_result = cleaning_ML(cleaned_data3)

model, battery_level, predicted_time_diff, Battery_level_train, Battery_level_test, Time_difference_train, Time_difference_test = Machine_Learning(
    cleaning_ML_result)

# Plot other figures using cleaned_data and cleaned_data2
fig = plot_line_chart(cleaned_data)
fig2 = bar_charging(cleaned_data)
fig3 = bar_device_usage(cleaned_data2)
# Call ML_plot with the results from Machine_Learning
fig4 = ML_plot(model, battery_level, predicted_time_diff, Battery_level_train, Battery_level_test,
               Time_difference_train, Time_difference_test)
# Table header
table_header = [
    html.Thead(html.Tr([html.Th("Information sur le terminal"), html.Th("Resultat")]),
               style={'background-color': '#ff7900'})
]

battery_level_value = battery_level[0][0]
predicted_time_diff_value = predicted_time_diff[0]
hours = int(predicted_time_diff_value)
minutes = int((predicted_time_diff_value - hours) * 60)
#  Table body from the API
# table_body = [
#     html.Tbody([
#         html.Tr([html.Td("Constructeur"), html.Td(device.get('make'))]),
#         html.Tr([html.Td("Code du model"), html.Td(device.get('model'))]),
#         html.Tr([html.Td("Nom du model"), html.Td(device.get('name'))], ),
#         html.Tr([html.Td("type de Operating System"), html.Td(device.get('os_type'))]),
#         html.Tr([html.Td("Status batterie"), html.Td(device.get('battery_status'))]),
#         html.Tr([html.Td("température batterie"), html.Td(device.get('battery_temp_in_celsius'))]),
#         html.Tr([html.Td("RAM utilsée"), html.Td(device.get('ram_usage'))]),
#         html.Tr([html.Td("RAM disponible"), html.Td(device.get('total_ram_size'))])
#     ])
# ]
# Table body
table_body = [
    html.Tbody([
        html.Tr([html.Td("Constructeur"), html.Td("Xiomi")]),
        html.Tr([html.Td("Code du model"), html.Td("23021RAAEG")]),
        html.Tr([html.Td("Nom du model"), html.Td("Redmi12")], ),
        html.Tr([html.Td("type de Operating System"), html.Td("Android")]),
        html.Tr([html.Td("Status batterie"), html.Td("69")]),
        html.Tr([html.Td("température batterie"), html.Td("23")]),
        html.Tr([html.Td("RAM utilsée"), html.Td("2317")]),
        html.Tr([html.Td("RAM disponible"), html.Td("3651")])
    ])
]

# Table component
table = dbc.Table(table_header + table_body,
                  bordered=True,
                  dark=False,
                  hover=True,
                  responsive=True,
                  striped=True)

app.layout = html.Div(style={'display': 'flex', 'align-items': 'flex-start'}, children=[
    # Sidebar with smartphone image and table
    dbc.Card(style={'width': '33%', 'padding': '28px'}, children=[
        dbc.CardImg(src="assets/smartphone.jpg", top=True, style={'opacity': 0.3}),
        dbc.CardBody([
            html.P(table)
        ])
    ]),
    # Main content area
    html.Div(style={'width': '67%', 'padding': '30px'}, children=[
        html.P(
            f"The battery level is {battery_level_value} and it can last up to approximately {hours} hours and {minutes} minutes to 30%."),
        # Dropdown component for selecting day
        dcc.Dropdown(
            id='day-dropdown',
            options=[{'label': day, 'value': day} for day in cleaned_data['Date (UTC)'].unique()],
            value=cleaned_data['Date (UTC)'].iloc[0]  # Set default value to first day
        ),
        # Graph components for displaying line chart and bar charts
        dcc.Graph(id='line-chart', figure=fig),
        dcc.Graph(id='bar-chart', figure=fig2),
        dcc.Graph(id='bar-chart2', figure=fig3),
        dcc.Graph(id='ml-plot', figure=fig4),
        dcc.Store(id='fig3-store', data=fig3)
    ])
])


# Define callback to update line chart based on selected day
@app.callback(
    Output('line-chart', 'figure'),
    [Input('day-dropdown', 'value')]
)
def update_line_chart(selected_day):
    # Filter cleaned_data DataFrame for the selected day
    filtered_df = cleaned_data[cleaned_data['Date (UTC)'] == selected_day]
    # Generate line chart based on filtered data
    fig = plot_line_chart(filtered_df)
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
