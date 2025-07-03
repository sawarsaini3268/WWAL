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

# normalize Billing Amount using Z-Score Standardization
if 'Billing Amount' in df.columns:
    mean_val = df['Billing Amount'].mean()
    std_val = df['Billing Amount'].std()
    df['BillingAmount_zscore'] = (df['Billing Amount'] - mean_val) / std_val
    print("Billing Amount column is normalized using Z-Score Standardization.")

# binary mapping for simple categorical columns
binary_maps = {
    'Gender': {'Male': 0, 'Female': 1}
}

for col, mapping in binary_maps.items():
    if col in df.columns:
        df[f'{col}_encoded'] = df[col].map(mapping)
        print(f"{col} encoded as 0/1.")

# one-hot encoding for multi-category columns
one_hot_columns = ['Blood Type', 'Admission Type']

for col in one_hot_columns:
    if col in df.columns:
        dummies = pd.get_dummies(df[col], prefix=col.replace(" ", ""))
        df = pd.concat([df, dummies], axis=1)
        print(f"{col} one-hot encoded.")

# reference date for offset calculation
reference_date = datetime.datetime(1970, 1, 1)

# convert Date of Admission
if 'Date of Admission' in df.columns:
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], errors='coerce')
    df['AdmissionDate_offset'] = (df['Date of Admission'] - reference_date).dt.days
    print("Date of Admission converted to offset days.")

# convert Discharge Date
if 'Discharge Date' in df.columns:
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'], errors='coerce')
    df['DischargeDate_offset'] = (df['Discharge Date'] - reference_date).dt.days
    print("Discharge Date converted to offset days.")

# one-hot encoding for additional categorical columns
additional_one_hot_columns = ['Medical Condition', 'Medication', 'Test Results']

for col in additional_one_hot_columns:
    if col in df.columns:
        dummies = pd.get_dummies(df[col], prefix=col.replace(" ", ""))
        df = pd.concat([df, dummies], axis=1)
        print(f"{col} one-hot encoded.")

# save the normalized dataset directly to THE_datasets_cleaned folder
output_path = r'C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\healthcare_dataset_normalized.csv'

df.to_csv(output_path, index=False)
print(f"✅ Normalized dataset saved as: {output_path}")




