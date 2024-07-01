import csv
import os
import pandas as pd
from clean_ember_data import *

filename = 'C:\\Users\\WiersmaL\\OneDrive - AECOM\\Projects\\ember-wholesaleprices-allcountries.csv'
print(clean_ember_data(filename).head())
