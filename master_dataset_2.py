import pandas as pd

# Load the heart dataset
heart = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\trimmed\heart_2020_dataset_normalized_trimmed.csv")

# Show the first 50 column names
print(heart.columns[:50])

# Load the NPHA dataset
npha = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\trimmed\NPHA_doctor_visits_normalized_trimmed.csv")

# Show the first 50 column names
print(npha.columns[:50])






# import pandas as pd

# # loading all trimmed + normalized datasets
# healthcare_df = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\trimmed\healthcare_dataset_normalized_trimmed.csv")
# heart_df = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\trimmed\heart_2020_dataset_normalized_trimmed.csv")
# npha_df = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\trimmed\NPHA_doctor_visits_normalized_trimmed.csv")
# output_df = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\trimmed\output_file_cleaned_normalized_trimmed.csv")

# # choosing 3–5 important columns from each dataset
# healthcare_cols = [
#     "Gender_encoded",
#     "BloodType_AB+",
#     "AdmissionDate_offset",
#     "DischargeDate_offset"
# ]

# heart_cols = [
#     "AlcoholDrinking_encoded",
#     "DiffWalking_encoded",
#     "Stroke_encoded",
#     "Asthma_encoded",
#     "SleepTime_normalized"
# ]

# npha_cols = [
#     "Trouble Sleeping_normalized",
#     "Stress Keeps Patient from Sleeping_normalized",
#     "Bathroom Needs Keeps Patient from Sleeping_normalized"
# ]

# output_cols = [
#     'Age of caregiver - created',
#     'Final number of Care Recipients',
#     'Count of ADLs',
#     'Count of IADLs',
#     'Count of caregiving support activities - cargivers of children only [NEW 2020]'
# ]
# # 
# # extracting only those columns
# healthcare_sub = healthcare_df[healthcare_cols].reset_index(drop=True)
# heart_sub = heart_df[heart_cols].reset_index(drop=True)
# npha_sub = npha_df[npha_cols].reset_index(drop=True)
# output_sub = output_df[output_cols].reset_index(drop=True)

# # truncating all to the same number of rows (to allow horizontal merging)
# min_length = min(len(healthcare_sub), len(heart_sub), len(npha_sub), len(output_sub))
# healthcare_sub = healthcare_sub.iloc[:min_length]
# heart_sub = heart_sub.iloc[:min_length]
# npha_sub = npha_sub.iloc[:min_length]
# output_sub = output_sub.iloc[:min_length]

# # merge everything side-by-side (horizontally)
# master_df = pd.concat([healthcare_sub, heart_sub, npha_sub, output_sub], axis=1)

# # save to CSV
# master_df.to_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\WWAL_synthetic_master_dataset.csv", index=False)
