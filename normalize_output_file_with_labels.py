import pandas as pd
import json

# load dataset
df = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_not_cleaned\output_file_with_full_labels.csv")

# load column category JSON
with open(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\output_file\column_groups.json") as f:
    column_groups = json.load(f)

