# Dating Platform User Profile Analysis

This repository contains a collection of scripts for data collection, cleaning, analysis, and trust score computation of user profiles from a dating platform. The project aims to identify patterns, assess profile authenticity, and derive meaningful insights from the data.

## Overview

The project consists of several key components:

1. **Data Collection:**
   - Scripts to scrape user data from a dating website, extracting basic and detailed user profile information.
   - Asynchronous web scraping techniques are used for efficient data collection.

2. **Data Cleaning and Preprocessing:**
   - Standardizing fields, correcting spellings, and formatting text data.
   - Cleaning operations include handling missing values, text cleaning, language detection, and splitting multi-value fields.
   - Text processing using NLTK and SpellChecker to refine and process description fields.

3. **Trust Score Computation:**
   - Computing trust scores for users using the PageRank algorithm based on their network of connections.
   - Trust scores are recalculated by resetting initial values based on a subset of users.

4. **Exploratory Data Analysis (EDA):**
   - Analysis of user profiles to understand distributions of various attributes.
   - Comparative analysis of 'scam' versus 'normal' profiles to identify distinguishing features.
   - Meta-feature extraction from user descriptions for in-depth textual analysis.

5. **Visualization and Insights:**
   - Visual representations of data distributions and key attributes.
   - Extracting insights from text data, including the identification of top words and meta-features.


## Requirements

- pandas
- numpy
- matplotlib
- networkx
- nltk
- spellchecker
- asyncio
- playwright
- tqdm
- langdetect
- re
- unicodedata
