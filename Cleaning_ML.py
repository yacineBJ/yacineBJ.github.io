import pandas as pd


def cleaning_ML(filtered_data):
    data = []
    target_time = pd.to_datetime('2024-05-12 19:53:04')

    for index, row in filtered_data.iterrows():
        battery_level = row['Battery (%)']
        date_time = pd.to_datetime(row['Date (UTC)'] + pd.to_timedelta(row['Time']))

        # Calculate the time difference between the data point and the target time
        time_diff = (target_time - date_time).total_seconds() / 3600  # Convert seconds to hours

        data.append((battery_level, time_diff))

    df = pd.DataFrame(data, columns=['Battery Level', 'Time Difference (hours)'])
    df.to_csv("data_Device_usage.csv", header=True, index=False)
    return df
