import csv
import os
import pandas as pd

def clean_ember_data(filename, country_of_interest):
    df = pd.read_csv(filename)
    df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'])
    df = df.loc[df['Country'].isin([country_of_interest]),
                :]
    df = df.drop(
            ['ISO3 Code',
             'Datetime (Local)',
             'Country'],
             axis=1)
    df = df.set_index(['Datetime (UTC)'])
    #df = df[start_time:end_time]
    return df