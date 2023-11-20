import pandas as pd
from efficient_apriori import apriori


# Load the cleaned data
cleaned_data = pd.read_csv('../DatingAppData/dissimilarity/processed_data.csv', encoding='ISO-8859-1')

# Display the first few rows of the cleaned data
cleaned_data.head()

# Replace NaN values with 'Unknown'
cleaned_data_filled = cleaned_data.fillna('Unknown')

# Convert the dataframe into a transactional format
transactions = cleaned_data_filled.apply(lambda row: list(row), axis=1).tolist()

# Exclude the 'description' column from the transactions
transactions_no_description = [trans[:-2] + trans[-1:] for trans in transactions]

# Convert all items in transactions to strings
transactions_str = [[str(item) for item in trans] for trans in transactions_no_description]

# Use efficient_apriori to find frequent itemsets and association rules
itemsets, _ = apriori(transactions_str, min_support=0.01)

# Convert itemsets to DataFrame for better visualization
itemsets_df = pd.DataFrame([(key, value) for key, value in itemsets.items()], columns=['Length', 'Itemsets'])
itemsets_df['Support'] = itemsets_df['Itemsets'].apply(lambda x: list(x.values())[0])
itemsets_df['Items'] = itemsets_df['Itemsets'].apply(lambda x: list(x.keys())[0])
itemsets_df = itemsets_df.drop(columns=['Itemsets']).sort_values(by='Support', ascending=False)

print(itemsets_df)
