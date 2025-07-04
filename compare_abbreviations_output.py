import pandas as pd

# load the output mapping file (abbreviations + full labels)
mapping_df = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\output_mapping.csv")

# load your dataset to compare
data_df = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\output_file_with_labels.csv")

# get the list of abbreviations from the mapping file
expected_abbreviations = mapping_df['Abbreviation'].tolist()

# get the actual columns from your dataset
actual_columns = data_df.columns.tolist()

# check which dataset columns are missing in the mapping
missing_in_mapping = [col for col in actual_columns if col not in expected_abbreviations]

# check which mapping abbreviations don't appear in your dataset
extra_in_mapping = [abbr for abbr in expected_abbreviations if abbr not in actual_columns]

# print results
print(f"\nTotal columns in dataset: {len(actual_columns)}")
print(f"Total abbreviations in mapping file: {len(expected_abbreviations)}")

if missing_in_mapping:
    print("\n!!!Columns in dataset NOT found in mapping file:")
    print(missing_in_mapping)
else:
    print("\nAll dataset columns are covered by the mapping file.")

if extra_in_mapping:
    print("\n!!!Abbreviations in mapping file NOT present in dataset:")
    print(extra_in_mapping)
else:
    print("\nAll mapping abbreviations appear in the dataset.")
