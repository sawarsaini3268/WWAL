import pandas as pd
from pathlib import Path

# Define the paths to your uploaded datasets
dataset_files = {
    "healthcare": Path("/mnt/data/healthcare_dataset_normalized_trimmed.csv"),
    "heart": Path("/mnt/data/heart_2020_dataset_normalized_trimmed.csv"),
    "npha": Path("/mnt/data/NPHA_doctor_visits_normalized_trimmed.csv"),
    "output": Path("/mnt/data/output_file_cleaned_normalized_trimmed.csv")
}

# List to hold all column data
all_columns = []

# Loop through each dataset, load, and extract columns
for dataset_name, file_path in dataset_files.items():
    try:
        df = pd.read_csv(file_path)
        for col in df.columns:
            all_columns.append({
                "Dataset": dataset_name,
                "Column_Name": col
            })
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Create a DataFrame from collected columns
columns_df = pd.DataFrame(all_columns)

# Save to one combined CSV
output_file = Path("/mnt/data/ALL_dataset_columns_combined.csv")
columns_df.to_csv(output_file, index=False)

print(f"✅ Saved combined columns to: {output_file}")
