# Data Cleaning and Exploratory Data Analysis for Dating Platform User Profiles

This repository contains scripts for cleaning, analyzing, and exploring user profile data from a dating platform. The scripts address issues like spelling corrections, removal of non-English entries, and extraction of useful insights through exploratory data analysis (EDA).

## Overview

The scripts perform the following key operations:

1. **Data Cleaning:**
    - Cleans and standardizes user profile data, including handling of missing values, text cleaning, and splitting multi-value fields.
    - Utilizes NLTK and SpellChecker for text processing and language detection.
    - Identifies and separates profiles into 'scam' and 'normal' categories.

2. **Exploratory Data Analysis (EDA):**
    - Computes value counts and distributions for various attributes in the dataset.
    - Visualizes the top attributes and compares distributions between scam and normal profiles.
    - Analyzes text data in descriptions to extract top words and perform meta-feature analysis.

3. **Text Processing:**
    - Removes stopwords, applies stemming, and extracts unique words from user descriptions.
    - Transforms text data into a set of descriptors for further analysis.

4. **Meta-Feature Extraction and Comparison:**
    - Extracts meta-features like word count, unique word count, stop word count, mean word length, and character count from descriptions.
    - Compares these meta-features between scam and normal profiles to identify distinguishing characteristics.

## Requirements

- pandas
- numpy
- matplotlib
- nltk
- spellchecker
- tqdm
- re
- unicodedata (for removing accents)
- langdetect

## Usage

1. **Data Cleaning:** The script cleans the user profile data by standardizing fields, correcting spellings, and formatting text data.

2. **EDA and Visualization:** Performs exploratory data analysis to understand the data's structure and distribution. Visualizations are used to compare attributes across different profile types.

3. **Text Data Processing:** Processes text data from user profiles, focusing on descriptions to extract meaningful insights and patterns.

4. **Meta-Feature Analysis:** Analyzes descriptive text data to extract and compare meta-features, providing insights into differences between scam and normal profiles.

## Results

- The scripts provide a clean and standardized dataset of user profiles from a dating platform.
- The exploratory data analysis offers insights into the characteristics of scam versus normal profiles, which can be useful for further analysis or model building.
