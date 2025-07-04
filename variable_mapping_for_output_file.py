import pandas as pd
import pyreadstat

# Path to your .sav file
sav_file_path = r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\not_data\Data - 2020 CG in US Public Use file FINAL.sav"

# Read the .sav file and extract metadata
df, meta = pyreadstat.read_sav(sav_file_path)

# Create mapping of abbreviations to full labels
mapping_df = pd.DataFrame({
    'Abbreviation': meta.column_names,
    'FullLabel': meta.column_labels
})

# Save to CSV
output_path = r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\output_mapping.csv"
mapping_df.to_csv(output_path, index=False)

print(f"Mapping saved to {output_path}")
