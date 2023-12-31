# -*- coding: utf-8 -*-
"""EDA

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ciI36H-IpxOGG9CSrkCLvKMgAdVHWJ3G

# 0. Init
"""

import csv
import os
import json
import argparse
import random
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


from tqdm import tqdm

# # spelling
# from spellchecker import SpellChecker

# nltk
import nltk
from nltk.corpus import stopwords

# from nltk.stem import PorterStemmer
# from nltk.tokenize import word_tokenize

# # language detector
# from langdetect import detect
# from langdetect import DetectorFactory
# DetectorFactory.seed = 0

# 'here_for,'smoke','drink', 'match_age'
union_meta = ['scam','username','age','gender','location','ethnicity','occupation','marital_status','children','religion','sexual_orientation','sex', 'description']

scam_meta = ['email']

tqdm.pandas()
nltk.download('stopwords')
nltk.download('punkt')

all_profile = pd.read_csv("../data/processed_data.csv")

"""# EDA"""

value_counts_dict = {}
for column in all_profile.columns:
    value_counts_dict[column] = all_profile[column].value_counts(normalize=True) * 100

value_counts_df = pd.DataFrame(value_counts_dict)

# Plot the top 10 attributes for all_profile
top_10_attributes = value_counts_df.mean().nlargest(10)
top_10_attributes.plot(kind='bar', figsize=(10, 6))
plt.title('Top 10 Attributes by Percentage Value Count')
plt.xlabel('Attributes')
plt.ylabel('Percentage Value Count')
plt.show()

all_profile_scam = all_profile[all_profile['scam'] == 1]
all_profile_normal = all_profile[all_profile['scam'] == 0]

col_interest = ['age_bin','gender','location','ethnicity','occupation','marital_status','children','religion','sexual_orientation']

top_scam = {}
top_normal = {}

for col in col_interest:
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    all_profile_scam[col].value_counts(normalize=True).head(5).plot(kind='bar', ax=axes[0], title=f"Scam - {col}")
    top_scam[col] = all_profile_scam[col].value_counts(normalize=True).head(5)
    all_profile_normal[col].value_counts(normalize=True).head(5).plot(kind='bar', ax=axes[1], title=f"Normal - {col}")
    top_normal[col] = all_profile_normal[col].value_counts(normalize=True).head(5)
    plt.show()

all_profile.info()

# Separate the sets for scam and freq_item_set
scam_sets = all_profile[all_profile['scam'] == 1]['description_stem_set'].dropna()
normal_sets = all_profile[all_profile['scam'] == 0]['description_stem_set'].dropna()

# Step 1: Create {word, count=1} pair for each cell
word_counts = Counter()
for word_set in scam_sets:
    word_set = re.sub(r'[^a-zA-Z0-9\s]', '', word_set).split()
    word_counts.update(word_set)

# Step 2: Aggregate all counts at the word level for the entire column
word_counts_aggregated = dict(word_counts)

# Step 3: Get the top 5 words with their counts
top_words = dict(Counter(word_counts_aggregated).most_common(20))

words = list(top_words.keys())
counts = list(top_words.values())

# Creating the bar plot
plt.figure(figsize=(20, 6))
plt.bar(words, counts, color='pink')
plt.title('Top Words in Scam sets and Their Counts')
plt.xlabel('Words')
plt.ylabel('Counts')
plt.show()

# Step 1: Create {word, count=1} pair for each cell
word_counts = Counter()
for word_set in normal_sets:
    word_set = re.sub(r'[^a-zA-Z0-9\s]', '', word_set).split()
    word_counts.update(word_set)

# Step 2: Aggregate all counts at the word level for the entire column
word_counts_aggregated = dict(word_counts)

# Step 3: Get the top 5 words with their counts
top_words = dict(Counter(word_counts_aggregated).most_common(20))

words = list(top_words.keys())
counts = list(top_words.values())

# Creating the bar plot
plt.figure(figsize=(20, 6))
plt.bar(words, counts, color='skyblue')
plt.title('Top Words in Normal sets and Their Counts')
plt.xlabel('Words')
plt.ylabel('Counts')
plt.show()

# extract meta feature
stopwords = set(stopwords.words('english'))

def transform(df, col):
    df['word_count'] = df[col].apply(lambda x: len(str(x).split()))
    df['unique_word_count'] = df[col].apply(lambda x: len(set(str(x).split())))
    df['stop_word_count'] = df[col].apply(lambda x: len([w for w in str(x).lower().split() if w in stopwords]))
    df['mean_word_length'] = df[col].apply(lambda x: np.mean([len(w) for w in str(x).split()]))
    df['char_count'] = df[col].apply(lambda x: len(str(x)))
    return df

scam_sets = all_profile[all_profile['scam'] == 1][['description']].dropna()
normal_sets = all_profile[all_profile['scam'] == 0][['description']].dropna()

transformed_scam_df = transform(scam_sets, 'description')
transformed_normal_df = transform(normal_sets, 'description')

meta_feature_list = ['word_count', 'unique_word_count', 'stop_word_count', 'mean_word_length', 'char_count']
max_values = {'word_count': 600, 'unique_word_count': 300, 'stop_word_count': 300, 'mean_word_length': 20, 'char_count': 3000}
widths = [20, 10, 10, 1, 100]

from matplotlib.ticker import MaxNLocator

def plot_distribution(df1, df2, feature_list, max_values):
    fig, axes = plt.subplots(nrows=len(feature_list), ncols=2, figsize=(20, 5*len(feature_list)))

    for i, feature in enumerate(feature_list):
        ax1 = axes[i, 0]
        ax2 = axes[i, 1]

        ax1.hist(df1[feature], label='Scam', color='pink', width=widths[i])
        ax1.set_title(f'Scam - {feature}')
        ax1.legend()
        ax1.set_xlim([0, max_values[feature]])
        ax1.set_ylim([0, max(max(np.histogram(df1[feature])[0])+1000, max(np.histogram(df2[feature])[0])+1000)])
        ax1.tick_params(axis='x', labelsize=8)
        ax1.set_ylabel('Document Count')
        ax1.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))

        ax2.hist(df2[feature], label='Normal', color='skyblue', width=widths[i])
        ax2.set_title(f'Normal - {feature}')
        ax2.legend()
        ax2.set_xlim([0, max_values[feature]])
        ax2.set_ylim([0, max(max(np.histogram(df1[feature])[0])+1000, max(np.histogram(df2[feature])[0])+1000)])
        ax2.tick_params(axis='x', labelsize=8)
        ax2.set_ylabel('Document Count')
        ax2.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))

    plt.tight_layout()
    plt.show()

# Plot the distribution of meta features
plot_distribution(transformed_scam_df, transformed_normal_df, meta_feature_list, max_values)

transformed_scam_df[meta_feature_list].describe()

transformed_normal_df[meta_feature_list].describe()
