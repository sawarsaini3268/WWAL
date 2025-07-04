import pandas as pd

# load both files
labels_df = pd.read_csv(r'"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\output_file_with_labels.csv"')  # Labels mapping file
data_df = pd.read_csv(r'"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\output_file.csv"')                # Actual dataset file

# print column names from the actual dataset
print("Dataset Columns:")
print(data_df.columns.tolist())

# manually extract the abbreviations from your labels file
# if the abbreviation column is named 'Abbreviation', adjust as needed:
print("\nExpected Abbreviations from Labels File:")
print(labels_df['Abbreviation'].tolist())
