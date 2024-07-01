import csv
import os
import pandas as pd

def clean_ember_data(filename):
    df = pd.read_csv(filename)

    return df