from datetime import datetime
import pandas as pd
import os


def clean_data():
    os.chdir(r"C:\Users\LEGION\.spyder-py3\redmidashboard\DataSource")

    # Read each CSV file into a separate DataFrame
    battery_history02_03 = pd.read_csv('battery_history_report-02-03.csv')
    battery_history03_04 = pd.read_csv('battery_history_report-03-04.csv')
    battery_history04_05 = pd.read_csv('battery_history_report-04-05.csv')
    battery_history05_06 = pd.read_csv('battery_history_report-05-06.csv')
    battery_history06_07 = pd.read_csv('battery_history_report-06-07.csv')
    battery_history07_08 = pd.read_csv('battery_history_report-07-08.csv')
    battery_history08_09 = pd.read_csv('battery_history_report-08-09.csv')
    battery_history09_10 = pd.read_csv('battery_history_report-09-10.csv')
    battery_history10_11 = pd.read_csv('battery_history_report-10-11.csv')
    battery_history11_12 = pd.read_csv('battery_history_report-11-12.csv')
    battery_history12_13 = pd.read_csv('battery_history_report-12-13.csv')
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(
        [battery_history02_03, battery_history03_04, battery_history04_05, battery_history05_06, battery_history06_07
            , battery_history07_08, battery_history08_09, battery_history09_10, battery_history10_11,
         battery_history11_12
            , battery_history12_13],
        ignore_index=True)
    combined_df = combined_df.drop(columns=["Device Name", "Group", "IMEI-1", "IMEI-2", "Serial Number"])
    # Convert "Date (UTC)" to string format
    combined_df["Date (UTC)"] = combined_df["Date (UTC)"].astype(str)
    # Transform 12 AM to 00 AM
    combined_df.loc[(combined_df["Time (UTC)"].str.contains("AM")) & (
        combined_df["Time (UTC)"].str.startswith("12:")), "Time (UTC)"] = "00:" + \
                                                                          combined_df["Time (UTC)"].str.split(":").str[
                                                                              1] + ":" + \
                                                                          combined_df["Time (UTC)"].str.split(":").str[
                                                                              2]
    combined_df = combined_df.drop_duplicates()
    # Split the "Time (UTC)" column into two separate columns
    combined_df[["Time", "AM_PM"]] = combined_df["Time (UTC)"].str.split(' ', expand=True)

    # Drop the original "Time (UTC)" column
    combined_df.drop(columns=["Time (UTC)"], inplace=True)

    # Transform String data to Date format
    combined_df["Time"] = combined_df["Time"].apply(lambda x: datetime.strptime(x, '%H:%M:%S').strftime('%H:%M:%S'))

    # Transform 1:28:05 PM to 13:28:05
    for index, row in combined_df.iterrows():
        if row["AM_PM"] == "PM":
            hour, minute, second = map(int, row["Time"].split(":"))
            # Add 12 hours to the hour component
            hour += 12
            if hour == 24:
                hour = 12
            else:
                if hour == 12:
                    hour = 0

            combined_df.at[index, "Time"] = f"{hour:02d}:{minute:02d}:{second:02d}"
    combined_df.drop(columns=["AM_PM"], inplace=True)
    # Export the DataFrame to a CSV file
    combined_df.to_csv("combined_battery_history.csv", index=False)
    return combined_df


def clean_device_usage():
    # Change directory to where the files are located
    os.chdir(r"C:\Users\LEGION\.spyder-py3\redmidashboard\DataSource")

    # Read individual CSV files
    device_usage_02_03 = pd.read_csv("device_usage_report_02-05-to-03-05.csv")
    device_usage_03_04 = pd.read_csv("device_usage_report_03-05-to-04-05.csv")
    device_usage_04_05 = pd.read_csv("device_usage_report_04-05-to-05-05.csv")
    device_usage_05_06 = pd.read_csv("device_usage_report_05_05-to-06-05.csv")
    device_usage_06_07 = pd.read_csv("device_usage_report_06-05-to-07-05.csv")
    device_usage_07_08 = pd.read_csv("device_usage_report_07-05-to-08-05.csv")
    device_usage_08_09 = pd.read_csv("device_usage_report_08-05-to-09-05.csv")
    device_usage_09_010 = pd.read_csv("device_usage_report_09-05-to-10-05.csv")
    device_usage_010_011 = pd.read_csv("device_usage_report_10-05-to-11-05.csv")
    device_usage_011_012 = pd.read_csv("device_usage_report_11-05-to-12-05.csv")
    device_usage_012_013 = pd.read_csv("device_usage_report_12-05-to-13-05.csv")

    # Concatenate all dataframes
    combined_df2 = pd.concat([
        device_usage_02_03, device_usage_03_04, device_usage_04_05, device_usage_05_06, device_usage_06_07,
        device_usage_07_08, device_usage_08_09, device_usage_09_010, device_usage_010_011, device_usage_011_012,
        device_usage_012_013
    ])
    # Split Date Range into Start_Date and End_Date
    combined_df2[["Start_Date", "End_Date"]] = combined_df2["Date Range"].str.split(' - ', expand=True)

    # Drop unnecessary columns
    combined_df2 = combined_df2.drop(
        columns=["Device Name", "Group", "IMEI Number", "Serial Number", "Device usage as JSON", "Date Range"])

    # Remove 'UTC' from all columns
    combined_df2 = combined_df2.replace('UTC', '', regex=True)
    combined_df2 = combined_df2.replace('Minutes', "", regex=True)
    # Convert all columns to numeric (errors='coerce' will replace non-convertible values with NaN)

    # Save the cleaned dataframe to CSV
    combined_df2.to_csv("combined_Device_usage.csv", header=True, index=False)

    return combined_df2


# this function to filter data from day 10-11-12
def clean_data2(combined_df):

    # Convert the 'Date (UTC)' column to datetime type
    combined_df['Date (UTC)'] = pd.to_datetime(combined_df['Date (UTC)'], format='%d-%b-%Y')

    # Define start and end dates and times
    start_date = '2024-05-10'
    end_date = '2024-05-12'
    start_time = '22:11:41'
    end_time = '19:53:04'

    # Filter the dataframe based on the date and time range
    filtered_data = combined_df[(combined_df['Date (UTC)'] == start_date) &
                                (combined_df['Time'] >= start_time) |
                                ((combined_df['Date (UTC)'] > start_date) &
                                 (combined_df['Date (UTC)'] < end_date)) |
                                ((combined_df['Date (UTC)'] == end_date) &
                                 (combined_df['Time'] <= end_time))]
    filtered_data.to_csv("filtered_battery_history.csv", index=False)
    return filtered_data