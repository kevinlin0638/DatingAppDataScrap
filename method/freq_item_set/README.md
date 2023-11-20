# Market Basket Analysis for Dating App Data

This repository contains scripts for conducting market basket analysis on a dating app dataset. The primary goal is to identify patterns in user attributes, focusing on the distinction between scam and non-scam profiles.

## Overview

The scripts perform the following key operations:

1. **Data Loading and Preprocessing:**
    - Loads a dataset and preprocesses it by handling missing values and converting data into a suitable format for analysis.

2. **Market Basket Analysis:**
    - Utilizes the Apriori algorithm to identify frequent itemsets and derive association rules.
    - Separates the data into scam and non-scam profiles for targeted analysis.

3. **Rule Filtering and Analysis:**
    - Filters out common rules between scam and non-scam profiles to find distinct patterns.
    - Ranks and selects the top rules for further insights.
   
## Requirements

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- efficient_apriori
- mlxtend
- nltk

## Usage

1. **Data Preparation:** The data is cleaned, NaN values are replaced, and the data is transformed into a transactional format suitable for market basket analysis.

2. **Apriori Algorithm:** The Apriori algorithm is applied to the transactional data to find frequent itemsets and generate association rules, separately for scam and non-scam profiles.

3. **Rule Analysis:** Distinct rules for scam and non-scam profiles are identified and the top rules are selected for further analysis.

## Results

- The analysis results in distinct sets of rules for scam and non-scam profiles.
- The validation process provides insights into the accuracy and effectiveness of the rules in classifying new profiles.
