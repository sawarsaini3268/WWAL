import pandas as pd

# load file 
file_path = r"C:\Users\sawar\OneDrive\UN_LearningPlanet\dataset_analysis\not_data\Full_List_of_Columns_for_Categorization.csv.xlsx"
df = pd.read_excel(file_path)

# clean the Category column (removes extra spaces)
df['Category_clean'] = df['Category'].str.strip()


