# import libraries
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# load dataset
filename = r'C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\heart_2020_cleaned.csv'

df = pd.read_csv(filename)
print("File loaded successfully.")
print(df.columns)

# normalize numeric columns using Min-Max Scaling
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

# list of columns to normalize
numeric_cols = ['BMI', 'PhysicalHealth', 'MentalHealth', 'SleepTime']

for col in numeric_cols:
    if col in df.columns:
        df[col + '_normalized'] = scaler.fit_transform(df[[col]])
        print(f"{col} column normalized using Min-Max Scaling.")
