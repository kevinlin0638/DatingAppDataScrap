from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules
import pandas as pd


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

# Transaction encoding
te = TransactionEncoder()
te_ary = te.fit(transactions_str).transform(transactions_str)
df_trans_encoded = pd.DataFrame(te_ary, columns=te.columns_)

# Apply Apriori algorithm
frequent_itemsets = apriori(df_trans_encoded, min_support=0.01, use_colnames=True)

print(frequent_itemsets.sort_values(by="support", ascending=False))

# Generate association rules from frequent itemsets
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
print(rules)