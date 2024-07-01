import csv
import os
import pandas as pd

def clean_ember_data(filename):
    df = pd.read_csv(filename)
    df['Datetime (Local)'] = pd.to_datetime(df['Datetime (Local)'])
    df = df[df['Datetime (Local)'].dt.year == 2023]
    df = df.assign(
        Month = df['Datetime (Local)'].dt.month,
        Day = df['Datetime (Local)'].dt.day,
        Hour = df['Datetime (Local)'].dt.hour).drop(
            ['ISO3 Code',
             'Datetime (UTC)',
             'Datetime (Local)'],
             axis=1)

    return df