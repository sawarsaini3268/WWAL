import pandas as pd

# load file 
file_path = r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\not_data\Full_List_of_Columns_for_Categorization.csv.xlsx"
df = pd.read_excel(file_path)

# clean the Category column (removes extra spaces)
df['Category_clean'] = df['Category'].str.strip()

# extracting lists 
# drop columns
drop_columns = df[df['Category_clean'] == 'Drop']['Column Name'].tolist()

# date columns
date_columns = df[df['Category_clean'] == 'Date']['Column Name'].tolist()

# categorical columns
categorical_columns = df[df['Category_clean'] == 'Categorical']['Column Name'].tolist()

# numerical (Min-Max)
minmax_columns = df[df['Category_clean'] == 'Numerical (Min-Max scaling)']['Column Name'].tolist()

# numerical (Z-score)
zscore_columns = df[df['Category_clean'] == 'Numerical (Z-score scaling)']['Column Name'].tolist()



