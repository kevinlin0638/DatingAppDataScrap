# Scam Detection in Dating Platform User Profiles

This repository contains scripts for the evaluation and combination of multiple scoring methods to classify user profiles on a dating platform as scam or non-scam. The project leverages a variety of scores including FIS (Frequent Item Set) scores, clustering scores, trust scores, and community scores.

## Overview

The scripts perform the following key operations:

1. **Score Calculation and Aggregation:**
   - FIS, clustering, trust, and community scores are read from respective CSV files.
   - These scores are cleaned, reformatted, and combined into a single DataFrame.

2. **Data Preparation:**
   - Scores are standardized and missing values are filled.
   - A combined score is calculated by summing the individual scores for each user profile.

3. **Sampling and Distribution Analysis:**
   - Separate subsets for scam and non-scam profiles are created.
   - Score distributions for both subsets are visualized and analyzed.

4. **Classification and Validation:**
   - A combined score threshold is used to classify profiles as scam or non-scam.
   - A confusion matrix is generated to validate the classification results.
   - The percentage of correct predictions and coverage of the scores is calculated.

## Requirements

- pandas
- numpy
- matplotlib
- seaborn
- tqdm
- scikit-learn

## Usage

1. **Score Integration:** Run the scripts to load and combine the different scores from FIS, clustering, trust, and community analysis.

2. **Data Preparation and Analysis:** Execute the scripts to prepare the combined dataset and analyze the distribution of scores.

3. **Classification and Validation:** Utilize the combined score to classify profiles and validate the results using a confusion matrix and other metrics.

## Results

- The project produces a comprehensive methodology to classify user profiles as scam or non-scam based on multiple scoring mechanisms.
- Visualization of score distributions provides insights into the distinct characteristics of scam and non-scam profiles.
- The confusion matrix and accuracy metrics offer a clear evaluation of the classification model's performance.
