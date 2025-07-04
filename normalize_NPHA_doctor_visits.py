# import libraries
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# load dataset
filename = r'C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\NPHA-doctor-visits.csv'
df = pd.read_csv(filename)

print("File loaded successfully.")
print(df.columns.tolist()) # add .toList() to print the full list of column names exactly as pandas reads them

# min-max scaling (normalize numerical columns)
scaler = MinMaxScaler()

# list of columns to normalize
columns_to_normalize = ['Age', 'Physical Health', 'Mental Health', 'Stress Keeping', 'Bathroom', 'Trouble Sleeping']

for col in columns_to_normalize:
    if col in df.columns:
        df[f"{col}_normalized"] = scaler.fit_transform(df[[col]])
        print(f"{col} column normalized using Min-Max Scaling.")

# one-hot encode categorical columns
categorical_columns = ['Race', 'Gender']

for col in categorical_columns:
    if col in df.columns:
        dummies = pd.get_dummies(df[col], prefix=col.replace(" ", ""), drop_first=False)
        df = pd.concat([df, dummies], axis=1)
        print(f"{col} column one-hot encoded.")

# full dataset with original + normalized columns
output_full = r'C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\NPHA_doctor_visits_normalized.csv'
df.to_csv(output_full, index=False)
print(f"Full dataset saved to {output_full}")

# trimmed dataset with only normalized/encoded columns
keep_columns = ['Number of Doctors Visited'] + \
               [f"{col}_normalized" for col in columns_to_normalize] + \
               [col for col in df.columns if any(prefix in col for prefix in ['Race_', 'Gender_'])]

df_trimmed = df[keep_columns]

output_trimmed = r'C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\NPHA_doctor_visits_normalized_trimmed.csv'
df_trimmed.to_csv(output_trimmed, index=False)
print(f"Trimmed dataset saved to {output_trimmed}")
