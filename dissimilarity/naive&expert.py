import json
import re
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from nltk import download as nltk_download
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Prepare necessary NLTK resources
nltk_download('punkt')
nltk_download('stopwords')

# Define file paths for inputs and outputs
PCC_RESULTS_FILE = 'pcc_results.json'
ALL_PROFILE_FILE = 'all_profile.csv'
NAIVE_SET_FILE = 'naive_set.csv'
EXPERT_SET_FILE = 'expert_set.csv'
NAIVE_WORD_COUNTS_PLOT = 'naive_word_counts.png'
EXPERT_WORD_COUNTS_PLOT = 'expert_word_counts.png'
META_FEATURE_DISTRIBUTION_PLOT = 'meta_feature_distribution.png'
NAIVE_SUMMARY_FILE = 'naive_summary.csv'
EXPERT_SUMMARY_FILE = 'expert_summary.csv'

# Load PCC results and profile data
with open(PCC_RESULTS_FILE, 'r') as file:
    pcc_results = json.load(file)
all_profile = pd.read_csv(ALL_PROFILE_FILE, index_col=0)

# Split profiles into scammers and normals
scammer_profiles = all_profile[all_profile['scam'] == 1]

# Calculate and sort average PCC scores for scam profiles
average_pcc_scores = {idx: np.mean(scores) for idx, scores in pcc_results.items()}
sorted_pcc = sorted(average_pcc_scores.items(), key=lambda item: item[1], reverse=True)

# Identify top and bottom 10% scam profiles
top_bottom_count = len(sorted_pcc) // 10
naive_set = sorted_pcc[:top_bottom_count]
expert_set = sorted_pcc[-top_bottom_count:]

# Save naive and expert sets to CSV
pd.DataFrame(naive_set, columns=['index', 'avg_pcc']).to_csv(NAIVE_SET_FILE, index=False)
pd.DataFrame(expert_set, columns=['index', 'avg_pcc']).to_csv(EXPERT_SET_FILE, index=False)

# Function to clean and count words in descriptions
def count_words(descriptions):
    counter = Counter()
    for desc in descriptions:
        words = word_tokenize(re.sub(r'[^a-zA-Z0-9\s]', '', desc).lower())
        counter.update(words)
    return counter

# Extract indices and convert string indices to integers
naive_indices = [int(idx) for idx, _ in naive_set]
expert_indices = [int(idx) for idx, _ in expert_set]

# Use the extracted indices to count words for naive and expert descriptions
naive_word_counts = count_words(scammer_profiles.loc[naive_indices, 'description'])
expert_word_counts = count_words(scammer_profiles.loc[expert_indices, 'description'])

def plot_word_counts(word_counts, title, color, filename):
    top_words = dict(word_counts.most_common(20))
    plt.figure(figsize=(20, 6))
    plt.bar(top_words.keys(), top_words.values(), color=color)
    plt.title(title)
    plt.xlabel('Words')
    plt.ylabel('Counts')
    plt.savefig(filename)
    plt.show()

# Plot and save word count bar plots
plot_word_counts(naive_word_counts, 'Top Words in Naive Sets', 'orange', NAIVE_WORD_COUNTS_PLOT)
plot_word_counts(expert_word_counts, 'Top Words in Expert Sets', 'purple', EXPERT_WORD_COUNTS_PLOT)

# Define function to extract and plot meta features
def extract_meta_features(df, text_col):
    stop_words = set(stopwords.words('english'))
    features = {
        'word_count': lambda x: len(x.split()),
        'unique_word_count': lambda x: len(set(x.split())),
        'stop_word_count': lambda x: sum(word in stop_words for word in x.lower().split()),
        'mean_word_length': lambda x: np.mean([len(word) for word in x.split()]),
        'char_count': len
    }
    for feature, func in features.items():
        df[feature] = df[text_col].apply(func)
    return df

# Apply transformations to naive and expert sets
transformed_naive_df = extract_meta_features(scammer_profiles.loc[naive_indices], 'description')
transformed_expert_df = extract_meta_features(scammer_profiles.loc[expert_indices], 'description')

# Save the meta features summaries to CSV files
transformed_naive_df.describe().to_csv(NAIVE_SUMMARY_FILE)
transformed_expert_df.describe().to_csv(EXPERT_SUMMARY_FILE)
