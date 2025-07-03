# import my libraries 
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# debugging
print("Starting script...")

#load dataset
filename = r'C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\healthcare_dataset.csv'
df = pd.read_csv(filename)

#debugging 
print("File loaded successfully.")

# check the available columns
print(df.columns)

# normalize Age using Min-Max Scaling
if 'Age' in df.columns:
    scaler_age = MinMaxScaler()
    df['Age_normalized'] = scaler_age.fit_transform(df[['Age']])
    print("Age column is normalized using Min-Max Scaling.")

