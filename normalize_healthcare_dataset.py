# import my libraries 
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler, StandardScaler

#load dataset
filename = r'C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\healthcare_dataset.csv'
df = pd.read_csv(filename)

# check the available columns
print(df.columns)
