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

# one-hot encode categorical columns
categorical_cols = ['Sex', 'AgeCategory', 'Race', 'Diabetic', 'GenHealth']

for col in categorical_cols:
    if col in df.columns:
        dummies = pd.get_dummies(df[col], prefix=col.replace(" ", ""))
        df = pd.concat([df, dummies], axis=1)
        print(f"{col} column one-hot encoded.")

# encode HeartDisease as 0/1 for correlation (this is the target -- usually leave the target column unchanged)
if 'HeartDisease' in df.columns:
    df['HeartDisease_encoded'] = df['HeartDisease'].map({'Yes': 1, 'No': 0})
    print("HeartDisease column encoded as 0/1.")

# save full dataset with original + normalized columns
full_output_path = r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\heart_2020_dataset_normalized.csv"
df.to_csv(full_output_path, index=False)
print(f"Full dataset with original and normalized columns saved to {full_output_path}")

# create trimmed dataset with only normalized/encoded columns
trimmed_cols = [col for col in df.columns if (
    '_normalized' in col or
    '_encoded' in col or
    any(prefix in col for prefix in ['Sex_', 'AgeCategory_', 'Race_', 'Diabetic_', 'GenHealth_'])
)]

# include target column for correlation
trimmed_cols.append('HeartDisease_encoded')

df_trimmed = df[trimmed_cols]

# save trimmed dataset
trimmed_output_path = r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\heart_2020_dataset_normalized_trimmed.csv"
df_trimmed.to_csv(trimmed_output_path, index=False)
print(f"Trimmed dataset with only normalized/encoded columns saved to {trimmed_output_path}")



