import json
from collections import Counter
import pandas as pd

# Load the previously calculated Pearson Correlation Coefficients results
with open('pcc_results.json', 'r') as file:
    loaded_pcc_results = json.load(file)

# Load the all_profile DataFrame from the saved CSV file
all_profile = pd.read_csv('all_profile.csv', index_col=0)

# Extract normal profile indices from the loaded PCC results
normal_indices = [index for scores in loaded_pcc_results.values() for index, _ in scores]

# Count how often each normal profile index occurs
index_counts = Counter(normal_indices)

# Identify indices that are flagged more than twice as similar to scammer profiles
trusted_indices = [index for index, count in index_counts.items() if count > 2]

# Create a DataFrame with the indices of trusted normal profiles
trusted_profile = pd.DataFrame(trusted_indices, columns=['normal_profile_index'])

# Save the indices of trusted profiles to a CSV for future reference
trusted_profile.to_csv('trusted_profile.csv', index=False)

# Retrieve detailed information for trusted profiles from the main dataset
trusted_profiles_info = all_profile.loc[trusted_profile['normal_profile_index'].astype(int)]

# Export the detailed trusted profile information to a CSV file
trusted_profiles_info.to_csv('trusted_profiles_info.csv', index=False)
