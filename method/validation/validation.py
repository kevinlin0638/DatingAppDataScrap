# -*- coding: utf-8 -*-

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/NUS_MSBA/CS5344/CS5344 project/scam score

import pandas as pd
import numpy as np
from functools import reduce

from tqdm import tqdm
tqdm.pandas()

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

fis_score = pd.read_csv("fis_scores.csv").set_index('username')
cluster_scores = pd.read_csv("cluster_scores.csv").set_index('username')
trust_score = pd.read_csv("trust_scores.csv").set_index('username')
community_scores = pd.read_csv("community_scores.csv").set_index('User')

# reformat
fis_score = fis_score.rename(columns={'marks': 'fis_score'})[['actual_class','fis_score']]
fis_score['actual_class'] = np.where(fis_score['actual_class'] == 'scam', 1, 0)
community_scores = community_scores.rename(columns={'Community Score': 'community_score'})

fis_score = fis_score.groupby(fis_score.index).mean()
cluster_scores = cluster_scores.groupby(cluster_scores.index).mean()

# join as 1 sample
dfs = [fis_score, cluster_scores, trust_score, community_scores]
full_scores = reduce(lambda left, right: pd.merge(left, right, how='left', left_index=True, right_index=True), dfs)

for i in dfs:
  print(i.info())

"""# Take sample"""

full_scores = full_scores.fillna(0)

score_col = ['fis_score', 'cluster_score', 'scaled_trust_score', 'community_score']
full_scores['sum_score'] = full_scores[score_col].sum(axis = 1)

seed = 99999
sample_size = 1000

scam_subset = full_scores[full_scores['actual_class'] == 1]
non_scam_subset = full_scores[full_scores['actual_class'] == 0]

scam_val = scam_subset.sample(n=sample_size, random_state=seed)
non_scam_val = non_scam_subset.sample(n=sample_size, random_state=seed)

full_val = pd.concat([scam_val, non_scam_val])

score_distribution_scam = scam_val['sum_score']
score_distribution_nonscam = non_scam_val['sum_score']

plt.rcParams['font.family'] = 'serif'

# Create subplots
fig, axes = plt.subplots(figsize=(10, 6))

# Plot the score distribution for scam samples in blue
axes.hist(score_distribution_scam, bins=20, alpha=0.6, color='black', label='Scam Samples')

# Plot the score distribution for non-scam samples in orange
axes.hist(score_distribution_nonscam, bins=20, alpha=0.6, color='grey', label='Non-Scam Samples')
axes.axvline(x=0, color='black', linestyle='--', linewidth=2, label='x=0')

# Set titles and labels
axes.set_title('Combined Score Distribution for Scam and Non-Scam Samples')
axes.set_xlabel('Total Score')
axes.set_ylabel('Frequency')

# Add legend
axes.legend()

# Show the plot
plt.show()

# Filter out samples with a score of 0
combined_samples_filtered = full_val[full_val['sum_score'] != 0]

# Predicted class based on marks
combined_samples_filtered['predicted_class'] = combined_samples_filtered['sum_score'].apply(lambda x: 'scam' if x < 0 else 'non-scam')
combined_samples_filtered['actual_class'] = combined_samples_filtered['actual_class'].apply(lambda x: 'scam' if x == 1 else 'non-scam')

# Create a confusion matrix
conf_matrix = confusion_matrix(combined_samples_filtered['actual_class'], combined_samples_filtered['predicted_class'], labels=['scam', 'non-scam'])

# Plot the confusion matrix using seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['scam', 'non-scam'], yticklabels=['scam', 'non-scam'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted Class')
plt.ylabel('True Class')
plt.show()

# Calculate percentage of samples with score != 0 for each dataset
percentage_not_zero_combined = (combined_samples_filtered.shape[0] / full_val.shape[0]) * 100
percentage_not_zero_scam = (scam_val[scam_val['sum_score'] != 0].shape[0] / scam_val.shape[0]) * 100
percentage_not_zero_nonscam = (non_scam_val[non_scam_val['sum_score'] != 0].shape[0] / non_scam_val.shape[0]) * 100

print(f"Percentage of samples with non-zero score in combined samples: {percentage_not_zero_combined:.2f}%")
print(f"Percentage of samples with non-zero score in scam samples: {percentage_not_zero_scam:.2f}%")
print(f"Percentage of samples with non-zero score in non-scam samples: {percentage_not_zero_nonscam:.2f}%")

# Calculate percentage of correct predictions for samples with score != 0
correct_predictions_combined = np.diag(conf_matrix).sum() / conf_matrix.sum() * 100
correct_predictions_scam = conf_matrix[0, 0] / conf_matrix[0, :].sum() * 100
correct_predictions_nonscam = conf_matrix[1, 1] / conf_matrix[1, :].sum() * 100

print(f"Percentage of correct predictions in combined samples with non-zero score: {correct_predictions_combined:.2f}%")
print(f"Percentage of correct predictions in scam samples with non-zero score: {correct_predictions_scam:.2f}%")
print(f"Percentage of correct predictions in non-scam samples with non-zero score: {correct_predictions_nonscam:.2f}%")