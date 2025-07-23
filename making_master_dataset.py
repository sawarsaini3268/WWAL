import pandas as pd

# loading all trimmed + normalized datasets
healthcare_df = pd.read_csv("THE_datasets_cleaned/healthcare_dataset_normalized_trimmed.csv")
heart_df = pd.read_csv("THE_datasets_cleaned/heart_2020_dataset_normalized_trimmed.csv")
npha_df = pd.read_csv("THE_datasets_cleaned/NPHA_doctor_visits_normalized_trimmed.csv")
output_df = pd.read_csv("THE_datasets_cleaned/output_file_cleaned_normalized_trimmed.csv")

# choosing 3–5 important columns from each dataset
healthcare_cols = [
    'Age_normalized',
    'BillingAmount_zscore',
    'Gender_encoded',
    'AdmissionDate_offset',
    'DischargeDate_offset'
]

heart_cols = [
    'BMI_normalized',
    'PhysicalHealth_normalized',
    'MentalHealth_normalized',
    'SleepTime_normalized',
    'PhysicalActivity_encoded'
]

npha_cols = [
    'Number of Doctors Visited',
    'Phyiscal Health_normalized',
    'Mental Health_normalized',
    'Stress Keeps Patient from Sleeping_normalized',
    'Bathroom Needs Keeps Patient from Sleeping_normalized'
]

output_cols = [
    'Age of caregiver - created',
    'Final number of Care Recipients',
    'Count of ADLs',
    'Count of IADLs',
    'Count of caregiving support activities - cargivers of children only [NEW 2020]'
]

# extracting only those columns
healthcare_sub = healthcare_df[healthcare_cols].reset_index(drop=True)
heart_sub = heart_df[heart_cols].reset_index(drop=True)
npha_sub = npha_df[npha_cols].reset_index(drop=True)
output_sub = output_df[output_cols].reset_index(drop=True)

# truncating all to the same number of rows (to allow horizontal merging)
min_length = min(len(healthcare_sub), len(heart_sub), len(npha_sub), len(output_sub))
healthcare_sub = healthcare_sub.iloc[:min_length]
heart_sub = heart_sub.iloc[:min_length]
npha_sub = npha_sub.iloc[:min_length]
output_sub = output_sub.iloc[:min_length]

# merge everything side-by-side (horizontally)
master_df = pd.concat([healthcare_sub, heart_sub, npha_sub, output_sub], axis=1)

# save to CSV
master_df.to_csv("THE_datasets_cleaned/WWAL_synthetic_master_dataset.csv", index=False)
