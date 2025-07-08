import pandas as pd
import json
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

# load dataset
df = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\output_file_with_full_labels.csv")

# load column category JSON
with open(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\output_file\column_groups.json") as f:
    column_groups = json.load(f)

# first drop the "Drop" columns, columns indicated in sorted json file
df.drop(columns=column_groups['drop'], inplace=True)

# double checking what got dropped
print("Dropped columns:", column_groups['drop'])

#convert the "Date" columns using datetime
for col in column_groups['date']:
    df[col] = pd.to_datetime(df[col], errors='coerce')  # convert and handle invalid dates

# double checking what got converted
print(df[column_groups['date']].dtypes)

# convert to string so numerical values aren't treated as continuous
for col in column_groups['categorical']:
    df[col] = df[col].astype(str)

# print dtypes BEFORE one-hot encoding to avoid losing the original columns
print("Categorical columns before one-hot encoding:")
print(df[column_groups['categorical']].dtypes)

# apply one-hot encoding
df = pd.get_dummies(df, columns=column_groups['categorical'], drop_first=True)

# prints a sample of the new columns
print("Sample of one-hot encoded columns:")
print(df.columns[df.columns.str.contains('_')][:10])  # just a peek


# min-max scaling
minmax_scaler = MinMaxScaler()
df[column_groups['minmax']] = minmax_scaler.fit_transform(df[column_groups['minmax']])

# double checking what got minmax-ed
print(df[column_groups['minmax']].dtypes) 

# z-score normalization (if any columns exist)
if column_groups["zscore"]:
    scaler = StandardScaler()
    df[column_groups["zscore"]] = scaler.fit_transform(df[column_groups["zscore"]])

# save full normalized version
df.to_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\output_file\output_file_cleaned_normalized.csv", index=False)
print("✅ Normalized dataset saved.")

# trim dataset 
df_trimmed = df.dropna()

# save trimmed version
df_trimmed.to_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\output_file\output_file_cleaned_normalized_trimmed.csv", index=False)
print("✂️ Normalized + Trimmed dataset saved.")

