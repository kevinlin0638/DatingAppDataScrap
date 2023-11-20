# -*- coding: utf-8 -*-

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

from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

tqdm.pandas()

all_profile = pd.read_csv("../../data/processed_data.csv")

"""# 2 Market Basket for Attributes"""

attribute_col = ['username','scam','age_bin','gender','location','ethnicity','marital_status','children','religion','sexual_orientation']
basket_col = ['scam','age_bin','gender','location','ethnicity','marital_status','children','religion','sexual_orientation']

all_profile_attribute = all_profile[attribute_col]
all_profile_attribute.dropna(subset=['username'], inplace=True)
all_profile_attribute.set_index('username', inplace=True)

# scam and non-scam
all_profile_attribute_scam = all_profile_attribute[all_profile_attribute['scam'] == 1]
all_profile_attribute_nonscam = all_profile_attribute[all_profile_attribute['scam'] == 0]

# change column value into "col name - value" format
def transform_row(row):
    return [f"{column} - {value}" for column, value in row.items() if pd.notna(value)]

all_profile_attribute_scam_b = all_profile_attribute_scam[basket_col].apply(transform_row, axis=1)
all_profile_attribute_nonscam_b = all_profile_attribute_nonscam[basket_col].apply(transform_row, axis=1)

def onehot_enc(df):
  encoder = TransactionEncoder().fit(df)
  onehot = encoder.transform(df)
  df = pd.DataFrame(onehot, columns = encoder.columns_)
  return df

all_profile_attribute_scam_enc = onehot_enc(all_profile_attribute_scam_b)
all_profile_attribute_nonscam_enc = onehot_enc(all_profile_attribute_nonscam_b)

# Run Apriori algorithm to find frequent itemsets
frequent_itemsets = apriori(all_profile_attribute_scam_enc, min_support=0.2, use_colnames=True)

# Generate association rules
scam_rules_raw = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
scam_rules_raw = scam_rules_raw[scam_rules_raw['consequents'] == {'scam - 1'}]

# Run Apriori algorithm to find frequent itemsets
frequent_itemsets = apriori(all_profile_attribute_nonscam_enc, min_support=0.2, use_colnames=True)

# Generate association rules
nonscam_rules_raw = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
nonscam_rules_raw = nonscam_rules_raw[nonscam_rules_raw['consequents'] == {'scam - 0'}]

# remove duplicates
scam_antecedents_set = set(scam_rules_raw['antecedents'])
nonscam_antecedents_set = set(nonscam_rules_raw['antecedents'])

scam_antecedents_set_processed = scam_antecedents_set - nonscam_antecedents_set
nonscam_antecedents_set_processed = nonscam_antecedents_set - scam_antecedents_set

scam_rules = scam_rules_raw[scam_rules_raw['antecedents'].isin(scam_antecedents_set_processed)]
nonscam_rules = nonscam_rules_raw[nonscam_rules_raw['antecedents'].isin(nonscam_antecedents_set_processed)]

scam_rules_top7 = scam_rules[['antecedents', 'consequents', 'support']].sort_values(by='support', ascending=False)

nonscam_rules_top7 = nonscam_rules[['antecedents', 'consequents', 'support']].sort_values(by='support', ascending=False)[:7]

scam_rules_top7 = [set(x) for x in scam_rules_top7['antecedents']]
nonscam_rules_top7 = [set(x) for x in nonscam_rules_top7['antecedents']]

scam_rules_top7.to_csv("scam_rules_top7.csv")
nonscam_rules_top7.to_csv("nonscam_rules_top7.csv")

samples_scam = pd.DataFrame(all_profile_attribute_scam_b)
samples_nonscam = pd.DataFrame(all_profile_attribute_nonscam_b)

def calculate_marks_row(row):
    sample = set(row[0])
    marks = 0

    for scam_rule in scam_rules_top7:
        l = len(scam_rule)
        if scam_rule <= sample:
            marks -= 0.5 * l

    for nonscam_rule in nonscam_rules_top7:
        l = len(nonscam_rule)
        if nonscam_rule <= sample:
            marks += 0.5 * l

    return marks

samples_scam['marks'] = samples_scam.progress_apply(calculate_marks_row, axis=1)
samples_nonscam['marks'] = samples_nonscam.progress_apply(calculate_marks_row, axis=1)

combined_samples = pd.concat([samples_scam, samples_nonscam], ignore_index=False)
combined_samples.to_csv('../DatingAppDataScrap/method/validation')