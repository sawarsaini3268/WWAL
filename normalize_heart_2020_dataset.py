# import libraries
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# load dataset
filename = r'C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\heart_2020_cleaned.csv'

df = pd.read_csv(filename)
print("File loaded successfully.")
print(df.columns)
