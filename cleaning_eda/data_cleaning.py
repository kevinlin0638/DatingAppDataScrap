# -*- coding: utf-8 -*-

import csv
import os
import json
import argparse
import random
import re
import pandas as pd
import numpy as np

from tqdm import tqdm

# spelling
from spellchecker import SpellChecker

# nltk
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# language detector
from langdetect import detect
from langdetect import DetectorFactory
DetectorFactory.seed = 0

# 'here_for,'smoke','drink', 'match_age'
union_meta = ['scam','username','age','gender','location','ethnicity','occupation','marital_status','children','religion','sexual_orientation','sex', 'description']

scam_meta = ['email']

nltk.download('stopwords')
nltk.download('punkt')

tqdm.pandas()

"""# 1. Clean-up"""

normal_profile = pd.read_csv('data.csv')
scam_profile1 = pd.read_csv('spam_output_female.csv')
scam_profile2 = pd.read_csv('spam_output_male.csv')
scam_profile = pd.concat([scam_profile1, scam_profile2])

# fix the scam description
def save_first_paragraph(text):
    if isinstance(text, str):
        text = text.split('IP')
        text = text[0]

        text = text.lower()
        text = text.split('ip address')
        text = text[0]

        text = text.split('message: – why is it a scam')
        text = text[0]

        text = text.split('message: –')
        text = text[0]

        text = text.split('why is it a scam')
        text = text[0]

        return text
    else:
        return None  # Return None if the cell is not a string

# Apply the function to the 'description' column
scam_profile['description'] = scam_profile['description'].progress_apply(save_first_paragraph)

# Create scam binary variable
normal_profile['scam'] = 0
scam_profile['scam'] = 1

# Standardise fields
normal_profile = normal_profile[union_meta]
scam_profile = scam_profile[union_meta]

# Union
all_profile = pd.concat([normal_profile, scam_profile])

# Convert into lowercase
all_profile = all_profile.astype(str)
all_profile = all_profile.applymap(lambda x: x.lower())

all_profile = all_profile.replace('nan', np.nan)

# Drop username = NaN
all_profile = all_profile.dropna(subset=['username'])

# Commented out IPython magic to ensure Python compatibility.
# %time
spell = SpellChecker()
column_to_check = ['ethnicity','marital_status','religion']

def correct_spelling(text):
    if pd.notnull(text) and isinstance(text, str):
        words = text.split()
        correct_words = [spell.correction(word) if word is not None else '' for word in words]
        correct_words = [str(word) for word in correct_words if word is not None]
        return ' '.join(correct_words)
    elif text is None:
        return ''
    else:
        return text

for col in column_to_check:
    print(col)
    all_profile[col] = all_profile[col].progress_apply(correct_spelling)
    print('Done!')

all_profile = all_profile.astype(str)

"""## Process attibutes"""

# List Unique value
def list_unique_values(df):
    for column in df.columns:
        unique_values = df[column].unique()
        count_values = len(unique_values)
        values_str = ', '.join(map(str, unique_values))
        print(f"{count_values} {column}: [{values_str}]")

list_unique_values(all_profile[union_meta[:-1]])

'''
1) remove wrong values and encode 0, 1 as nan
2) age: remove " y.o."
3) children:
   - i don’t have children >> no children
   - remove "i "
   - remove "have "
   - remove "children "
   - 1
'''

# Function to split 'x or y' values in specified columns
splitfields = ['occupation', 'ethnicity', 'marital_status']

temp_df = all_profile[all_profile[splitfields].progress_apply(lambda x: x.str.contains(' or ')).any(axis=1)]

# Delete original row from the full list
for col in splitfields:
  all_profile = all_profile[~all_profile[col].astype(str).str.contains(' or ')]

split_rows = []

for index, row in temp_df.iterrows():
    for field in splitfields:
        if ' or ' in row[field]:
            values = [val.strip() for val in row[field].split(' or ')]  # Splitting the row values
            for value in values:
                temp_row = row.copy()
                temp_row[field] = value.strip()
                split_rows.append(temp_row)

# Creating a new DataFrame from the list of split rows
split_df = pd.DataFrame(split_rows)

# Add the split row back
all_profile = pd.concat([all_profile,split_df])

# change age format
all_profile['age'] = all_profile['age'].astype(str).progress_apply(lambda x: x.replace(' y.o.', '')).astype(float)

# change 1, 0 into nan
encode_field = ['ethnicity', 'marital_status', 'religion', 'age', 'children', 'sexual_orientation']
for col in encode_field:
    all_profile[col] = all_profile[col].progress_apply(lambda x: np.nan if x == 1 or x == 0 else x)

# delete entry with wrongly filled value
delete_dict = {
               'ethnicity':['white', 'hispanic', 'mixed', 'asian', 'native american', 'black', 'middle eastern', 'pacific islander', 'other']
               ,'marital_status':['single', 'widowed', 'divorced', 'married', 'separated', 'in relationship']
               ,'religion': ['spiritual', 'christian', 'other', 'buddhist', 'atheist', 'muslim', 'jewish', 'hindu']
               ,'sexual_orientation': ['straight', 'bisexual', 'homosexual', 'sraight']
              }
for key, values in delete_dict.items():
    if len(values) > 0:
      all_profile.loc[~all_profile[key].isin(values), key] = np.nan

# replace 'nan' with np.nan
dall_profile = all_profile.replace('nan', np.nan)

# change children
all_profile['children'].replace('i don’t have children', 'no children', inplace=True)
all_profile['children'].replace('don’t children', 'don’t want children', inplace=True)
all_profile['children'] = all_profile['children'].astype(str).progress_apply(lambda x: x.replace('i ', ''))
all_profile['children'] = all_profile['children'].astype(str).progress_apply(lambda x: x.replace('have ', ''))

list_unique_values(all_profile[union_meta[:-1]])

# bin age
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Define the labels for the bins
labels = ['1-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']

# Use pd.cut to create the age bins
all_profile['age_bin'] = pd.cut(all_profile['age'], bins=bins, labels=labels, right=False)

# remove accents
import unicodedata

def remove_accents(text):
    if isinstance(text, str):
        nfkd_form = unicodedata.normalize('NFKD', text)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    else:
        return np.nan  # Return an empty string if the text is not a string

col_list = ['location', 'occupation']
for col in col_list:
  all_profile[col] = all_profile[col].progress_apply(remove_accents)


"""# 2. process occupation and description"""
# detect english
def is_english(text):
    try:
        words = text.split()
        first_10_words = " ".join(words[:10])
        # print(first_10_words)
        lang = detect(first_10_words)
        # print(f"Detected language: {lang}")
        return lang == 'en'
    except:
        return False

all_profile.loc[~all_profile['description'].progress_apply(is_english), 'description'] = np.nan

# remove stopwords
def remove_stopwords(text):
    if isinstance(text, str):  # Check if the text is a string
        stop_words = set(stopwords.words('english'))  # Set of English stopwords
        words = word_tokenize(text)
        filtered_words = [re.sub(r'[^a-zA-Z0-9\s]', '', word) for word in words if word.lower() not in stop_words]
        return ' '.join(filtered_words)
    else:
        return np.nan  # Return an empty string if the text is not a string

all_profile['description_set'] = all_profile['description'].progress_apply(remove_stopwords)

# stem
def stem_words(text):
    if isinstance(text, str):  # Check if the text is a string
        porter = PorterStemmer()
        token_words = word_tokenize(text)
        stem_sentence = [porter.stem(word) for word in token_words]
        return ' '.join(stem_sentence)
    else:
        return np.nan  # Return an empty string if the text is not a string

all_profile['description_stem'] = all_profile['description_set'].progress_apply(stem_words)

def extract_unique_words(text):
    if isinstance(text, str):
      return set(text.split())
    else:
        return np.nan

all_profile['description_set'] = all_profile['description_set'].progress_apply(extract_unique_words)
all_profile['description_stem_set'] = all_profile['description_stem'].progress_apply(extract_unique_words)

all_profile.to_csv("../DatingAppDataScrap/data/processed_data.csv")
