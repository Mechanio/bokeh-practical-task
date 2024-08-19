### NOT FULLY DONE TASK
### NOT FULLY DONE TASK
### NOT FULLY DONE TASK

import bokeh
import pandas as pd
import numpy as np

df = pd.read_csv("Titanic-Dataset.csv")
df.fillna(value={'Cabin': 'Unknown', 'Embarked': 'Unknown'}, inplace=True)  # Fill missing values
# df = df[df['Age'] > 0]
# or
df['Age'].interpolate(inplace=True)
df['AgeGroup'] = df['Age'].apply(lambda x: 'Child' if x < 18 else ('Young Adult' if x < 30 else ('Adult' if x < 60 else 'Senior')))
