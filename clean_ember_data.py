import pandas as pd

file = 'C:\Users\WiersmaL\OneDrive - AECOM\Projects\ember-wholesaleprices-allcountries.csv'
df = pd.read_csv(file)
print(df.head())
