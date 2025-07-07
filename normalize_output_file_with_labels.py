import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#load dataset
file_path = r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\output_file_with_full_labels.csv"
df = pd.read_csv(file_path, header=0)

# remove rows where the first column accidentally repeated the header name
first_col_name = df.columns[0]
df = df[df[first_col_name] != first_col_name]

print(f"Dataset shape after cleaning: {df.shape}") # shows (rows, columns) after cleaning

# count rows with at least one NaN value
nan_rows = df[df.isna().any(axis=1)]
nan_count = nan_rows.shape[0]
total_rows = df.shape[0]
nan_percentage = (nan_count / total_rows) * 100
print(f"Rows with at least one NaN: {nan_count} out of {total_rows} ({nan_percentage:.2f}%)")


# selective NaN handling for categorical columns 
categorical_columns = [
    "Age of Main Care Recipient categorical - created",
    "Age of caregiver categorical - created",
    "Asian caregiver flag",
    "Care recipient gender",
    "Caregiver Education highest grade completed - created",
    "Caregiver Household Income - created [in each year's dollars, no adjustment]",
    "Categorical hours of care provided - created",
    "Count of ADLs",
    "Count of IADLs",
    "Count of caregiving support activities - caregivers of children only [NEW 2020]",
    "D1 - Caregiver health status [at time of caregiving]",
    "D2 - Impact of caregiving on caregiver health status",
    "D4 - caregiver served in military - created (online) and asked (phone)",
    "D5 - Care recipient ever served in US Armed Forces [if adult recipient]",
    "D5b - Did recipient serve before 9-11-01 (if veteran; 2015 only)?",
    "D6 - Caregiver had children living in home [at time of caregiving]",
    "Does recipient live with caregiver - created",
    "Ever employed in past year while also a caregiver - created",
    "Final Caregiver Status flag at Household Level",
    "Final number of Care Recipients"
]

# replace NaN with 'Unknown' in those columns only
df[categorical_columns] = df[categorical_columns].fillna("Unknown")


# replaces categorical columns with binary indicator columns (0/1) (one-hot encoding)
df_encoded = pd.get_dummies(df, columns=categorical_columns, prefix_sep="_", drop_first=False)
print(f"One-hot encoding applied. New shape: {df_encoded.shape}")

# columns  for Min-Max scaling
min_max_columns = [
    "Total hours of care provided",
    "Age of caregiver (numeric)",
    "Age of Main Care Recipient (numeric)",
    "Caregiver Household Income (actual dollars)",
    "Count of ADLs",
    "Count of IADLs"
]

# only scale columns that exist in df_encoded to avoid errors
min_max_columns_present = [col for col in min_max_columns if col in df_encoded.columns]

# apply Min-Max scaling to those columns
scaler = MinMaxScaler()
df_encoded[min_max_columns_present] = scaler.fit_transform(df_encoded[min_max_columns_present])

print(f"Min-Max scaling applied to columns: {min_max_columns_present}")
print(f"Final dataset shape: {df_encoded.shape}")

output_path_normalized = r'C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\output_file_normalized.csv'
df_encoded.to_csv(output_path_normalized, index=False)
print(f"Normalized, cleaned dataset saved to: {output_path_normalized}")

