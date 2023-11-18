import json
from collections import Counter
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from matplotlib.ticker import MaxNLocator

# Load the PCC results from a JSON file
with open('pcc_results.json', 'r') as file:
    pcc_results = json.load(file)

# Load the all_profile DataFrame from the saved CSV file
all_profile = pd.read_csv('all_profile.csv', index_col=0)

# Get the scammer profiles
scammer_profiles = all_profile[all_profile['scam'] == 1]

# Calculate the average PCC score for each scam profile
average_pcc_scores = {scam_index: np.mean([score for _, score in scores])
                      for scam_index, scores in pcc_results.items()}

# Sort scammer profiles by average PCC score to identify similarity and dissimilarity
sorted_by_pcc = sorted(average_pcc_scores.items(), key=lambda item: item[1], reverse=True)

# Determine the top and bottom 10% of profiles
ten_percent_count = int(len(sorted_by_pcc) * 0.1)
naive_set = sorted_by_pcc[:ten_percent_count]
expert_set = sorted_by_pcc[-ten_percent_count:]

# Convert naive and expert sets to DataFrames and save them
naive_df = pd.DataFrame(naive_set, columns=['scam_profile_index', 'average_pcc_score'])
expert_df = pd.DataFrame(expert_set, columns=['scam_profile_index', 'average_pcc_score'])
naive_df.to_csv('naive_set.csv', index=False)
expert_df.to_csv('expert_set.csv', index=False)

# Map profile indices to actual profiles for further analysis
naive_sets_df = scammer_profiles.loc[naive_df.scam_profile_index]
expert_sets_df = scammer_profiles.loc[expert_df.scam_profile_index]

# Analyze word frequency in profile descriptions for naive and expert sets

# Step 1: Create {word, count=1} pair for each cell
naive_word_counts = Counter()
for word_set in naive_sets_df.description_stem_set:
    word_set = re.sub(r'[^a-zA-Z0-9\s]', '', word_set).split()
    naive_word_counts.update(word_set)

# Step 2: Aggregate all counts at the word level for the entire column
naive_word_counts_aggregated = dict(naive_word_counts)

# Step 3: Get the top 20 words with their counts
top_naive_words = dict(Counter(naive_word_counts_aggregated).most_common(20))

# Creating the bar plot for Naive Sets
plt.figure(figsize=(20, 6))
plt.bar(top_naive_words.keys(), top_naive_words.values(), color='orange')
plt.title('Top Words in Naive Sets and Their Counts')
plt.xlabel('Words')
plt.ylabel('Counts')
plt.savefig('naive_word_counts.png')  # Save the figure as an image file
plt.show()


# Step 1: Create {word, count=1} pair for each cell
expert_word_counts = Counter()
for word_set in expert_sets_df.description_stem_set:
    word_set = re.sub(r'[^a-zA-Z0-9\s]', '', word_set).split()
    expert_word_counts.update(word_set)

# Step 2: Aggregate all counts at the word level for the entire column
expert_word_counts_aggregated = dict(expert_word_counts)

# Step 3: Get the top 20 words with their counts
top_expert_words = dict(Counter(expert_word_counts_aggregated).most_common(20))

# Creating the bar plot for Expert Sets
plt.figure(figsize=(20, 6))
plt.bar(top_expert_words.keys(), top_expert_words.values(), color='purple')
plt.title('Top Words in Expert Sets and Their Counts')
plt.xlabel('Words')
plt.ylabel('Counts')
plt.savefig('expert_word_counts.png')  # Save the figure as an image file
plt.show()


# Transform dataframes with meta feature extraction
stopwords = set(stopwords.words('english'))

def transform(df, col):
    df['word_count'] = df[col].apply(lambda x: len(str(x).split()))
    df['unique_word_count'] = df[col].apply(lambda x: len(set(str(x).split())))
    df['stop_word_count'] = df[col].apply(lambda x: len([w for w in str(x).lower().split() if w in stopwords]))
    df['mean_word_length'] = df[col].apply(lambda x: np.mean([len(w) for w in str(x).split()]))
    df['char_count'] = df[col].apply(lambda x: len(str(x)))
    return df

# Apply transformations
transformed_naive_df = transform(naive_sets_df, 'description')
transformed_expert_df = transform(expert_sets_df, 'description')

# Define meta feature list and plotting parameters
meta_feature_list = ['word_count', 'unique_word_count', 'stop_word_count', 'mean_word_length', 'char_count']
max_values = {'word_count': 600, 'unique_word_count': 300, 'stop_word_count': 300, 'mean_word_length': 20, 'char_count': 3000}
widths = [20, 10, 10, 1, 100]

# Function to plot the distribution of meta features
def plot_distribution(df1, df2, feature_list, max_values):
    fig, axes = plt.subplots(nrows=len(feature_list), ncols=2, figsize=(20, 5*len(feature_list)))

    for i, feature in enumerate(feature_list):
        ax1 = axes[i, 0]
        ax2 = axes[i, 1]

        ax1.hist(df1[feature], label='Naive', color='orange', width=widths[i])
        ax1.set_title(f'Naive - {feature}')
        ax1.legend()
        ax1.set_xlim([0, max_values[feature]])
        ax1.set_ylim([0, max(max(np.histogram(df1[feature])[0])+1000, max(np.histogram(df2[feature])[0])+1000)])
        ax1.tick_params(axis='x', labelsize=8)
        ax1.set_ylabel('Document Count')
        ax1.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))

        ax2.hist(df2[feature], label='Expert', color='purple', width=widths[i])
        ax2.set_title(f'Expert - {feature}')
        ax2.legend()
        ax2.set_xlim([0, max_values[feature]])
        ax2.set_ylim([0, max(max(np.histogram(df1[feature])[0])+1000, max(np.histogram(df2[feature])[0])+1000)])
        ax2.tick_params(axis='x', labelsize=8)
        ax2.set_ylabel('Document Count')
        ax2.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))

    plt.tight_layout()
    plt.savefig('meta_feature_distribution.png')  # Save the figure as an image file
    plt.show()

# Plot the distribution of meta features for naive and expert sets
plot_distribution(transformed_naive_df, transformed_expert_df, meta_feature_list, max_values)

# Summarize meta features and save the summaries to CSV files
naive_summary = transformed_naive_df[meta_feature_list].describe()
naive_summary.to_csv('naive_summary.csv')  # Save the naive summary as a CSV file

expert_summary = transformed_expert_df[meta_feature_list].describe()
expert_summary.to_csv('expert_summary.csv')  # Save the expert summary as a CSV file