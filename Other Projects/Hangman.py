import pandas as pd

# Read data from a CSV file using the raw string approach where the file path has been copied and pasted as is and r is added before the source file path
df = pd.read_csv(r'C:\Users\ShreyJariwala\OneDrive\Desktop\1. Learning\Projects\Python\Placement Card - August 6, 2024.csv')

# Display the first few rows of the dataframe
print(df.head())


# Selecting a column
print(df['Job'])
