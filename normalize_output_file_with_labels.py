import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#load dataset
file_path = r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\output_file_with_full_labels.csv"
df = pd.read_csv(file_path, header=0)

#strip spaces from all column names to avoid KeyErrors due to hidden spaces
df.columns = df.columns.str.strip()

