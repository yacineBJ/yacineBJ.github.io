import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def Machine_Learning(df):
    Battery_level = df[['Battery Level']]  # Using double square brackets to select as DataFrame
    Time_difference = df['Time Difference (hours)']

    # Adjusting random_state to None
    Battery_level_train, Battery_level_test, Time_difference_train, Time_difference_test = train_test_split(
        Battery_level, Time_difference, test_size=0.2, random_state=None)

    model = LinearRegression()
    model.fit(Battery_level_train, Time_difference_train)

    score = model.score(Battery_level_test, Time_difference_test)
    print("Model score:", score)
    battery_level = np.array([[69]])
    predicted_time_diff = model.predict(battery_level)
    print("Predicted time difference for battery level", battery_level, " : ", predicted_time_diff)
    return model,battery_level, predicted_time_diff, Battery_level_train, Battery_level_test, Time_difference_train, Time_difference_test
