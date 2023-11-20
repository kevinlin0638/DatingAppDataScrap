import pandas as pd

data = pd.read_csv('../DatingAppData/dissimilarity/processed_data.csv', encoding='ISO-8859-1')

# Display the first few rows of the data
data.head()

# Distribution of the 'scam' column
scam_distribution = data['scam'].value_counts(normalize=True) * 100
print(scam_distribution)

# Summary statistics for numeric columns
numeric_summary = data.describe()
print(numeric_summary)

# Number of missing values in each column
missing_values = data.isnull().sum()
print(missing_values)

# Distribution of 'gender', 'ethnicity', and 'marital_status' columns
gender_distribution = data['gender'].value_counts(normalize=True) * 100
ethnicity_distribution = data['ethnicity'].value_counts(normalize=True) * 100
marital_status_distribution = data['marital_status'].value_counts(normalize=True) * 100
print(gender_distribution, ethnicity_distribution, marital_status_distribution)
