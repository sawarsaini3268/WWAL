
# # Load the heart dataset
# heart = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\trimmed\heart_2020_dataset_normalized_trimmed.csv")

# # Show the first 50 column names
# print(heart.columns[:50])

# # Load the NPHA dataset
# npha = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\trimmed\NPHA_doctor_visits_normalized_trimmed.csv")

# # Show the first 50 column names
# print(npha.columns[:50])

import pandas as pd
import matplotlib.pyplot as plt
import os

# load datasets
heart = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\trimmed\heart_2020_dataset_normalized_trimmed.csv")
healthcare = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\trimmed\healthcare_dataset_normalized_trimmed.csv")
npha = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\trimmed\NPHA_doctor_visits_normalized_trimmed.csv")
output = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\trimmed\output_file_cleaned_normalized_trimmed.csv")

# select new columns
df_healthcare = healthcare[[
    "BillingAmount_zscore",
    "TestResults_Abnormal",
    "MedicalCondition_Cancer",
    "Age_normalized"
]].reset_index(drop=True)

df_heart = heart[[
    "MentalHealth_normalized",
    "DiffWalking_encoded",
    "SleepTime_normalized",
    "HeartDisease_encoded"
]].reset_index(drop=True)

df_npha = npha[[
    "Number of Doctors Visited",
    "Trouble Sleeping_normalized",
    "Bathroom Needs Keeps Patient from Sleeping_normalized"
]].reset_index(drop=True)

df_output = output[[
    "Household size - created",
    "Q17 Count of conditions selected - created",
    "N16 count of benefits total - use for 2020 only - items A-F [employed caregivers only]",
    "Q34 - Count of workplace accomodations made"
]].reset_index(drop=True)

# align by shortest length
min_len = min(len(df_healthcare), len(df_heart), len(df_npha), len(df_output))
df_healthcare = df_healthcare.iloc[:min_len]
df_heart = df_heart.iloc[:min_len]
df_npha = df_npha.iloc[:min_len]
df_output = df_output.iloc[:min_len]

# horizontally merge
merged_df = pd.concat([df_healthcare, df_heart, df_npha, df_output], axis=1)

# save merged dataset
os.makedirs("THE_datasets_cleaned", exist_ok=True)
merged_df.to_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\merged_synthetic_datasets\WWAL_synthetic_master_dataset_2.csv", index=False)
print("new synthetic dataset saved!")

# correlation function
correlation_matrix = merged_df.corr()

# print results
print(correlation_matrix)

# save to CSV so that i can review or share
correlation_matrix.to_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\correlation_files\WWAL_correlation_matrix_2.csv")
