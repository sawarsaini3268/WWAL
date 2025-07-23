import pandas as pd

# load master dataset
df = pd.read_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\WWAL_synthetic_master_dataset.csv")

# correlation function
correlation_matrix = df.corr()

# print results
print(correlation_matrix)

# save to CSV so that i can review or share
correlation_matrix.to_csv(r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\THE_datasets_cleaned\correlation_files\WWAL_correlation_matrix.csv")
