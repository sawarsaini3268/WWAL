import pandas as pd

# Load both files
labels_df = pd.read_csv(r'"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\output_file_with_labels.csv"')  # Labels mapping file
data_df = pd.read_csv(r'"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\output_file.csv"')                # Actual dataset file

# Print column names from the actual dataset
print("Dataset Columns:")
print(data_df.columns.tolist())

# Manually extract the abbreviations from your labels file
# If the abbreviation column is named 'Abbreviation', adjust as needed:
print("\nExpected Abbreviations from Labels File:")
print(labels_df['Abbreviation'].tolist())
