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

# encode Yes/No columns as 0/1
yes_no_cols = [
    'Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking',
    'PhysicalActivity', 'Asthma', 'KidneyDisease', 'SkinCancer'
]

for col in yes_no_cols:
    if col in df.columns:
        df[col + '_encoded'] = df[col].map({'Yes': 1, 'No': 0})
        print(f"{col} column encoded as 0/1.")
