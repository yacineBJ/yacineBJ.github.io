import numpy as np
import plotly.graph_objects as go


def ML_plot(model,battery_level, predicted_time_diff, Battery_level_train, Battery_level_test, Time_difference_train,
            Time_difference_test):
    # Generate a range of x values for plotting
    x_range = np.linspace(Battery_level_train.min(), Battery_level_train.max(), 100).reshape(-1, 1)

    # Predict time differences for the entire x range
    predicted_range = model.predict(x_range)

    # Create a plotly figure
    fig = go.Figure()

    # Add training data points
    fig.add_trace(go.Scatter(x=Battery_level_train.squeeze(), y=Time_difference_train, name='Train', mode='markers'))

    # Add test data points
    fig.add_trace(go.Scatter(x=Battery_level_test.squeeze(), y=Time_difference_test, name='Test', mode='markers'))

    # Add prediction line
    fig.add_trace(go.Scatter(x=x_range.squeeze(), y=predicted_range, name='Prediction'))
    fig.update_xaxes(autorange='reversed')
    # Set plot title and axis labels
    fig.update_layout(title='Machine Learning Prediction',
                      xaxis_title='Battery Level',
                      yaxis_title='Time Difference (hours)')

    return fig
