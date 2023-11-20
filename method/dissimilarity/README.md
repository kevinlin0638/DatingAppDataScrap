# User Profile Analysis Toolkit

This collection of scripts is designed to analyze user profiles and calculate dissimilarity scores, 
identify trusted profiles, and differentiate between naive and expert user sets based on profile characteristics.

## Overview

The toolkit comprises three main scripts, which should be executed in the following order:

1. `dissimilarity_score.py` - Calculates the dissimilarity scores between user profiles.
2. `trusted_profile.py` - Identifies and extracts profiles that can be considered trusted based on the dissimilarity scores.
3. `naive&expert.py` - Segregates the profiles into naive and expert sets based on predefined criteria.

## Requirements

- Python 3.6 or higher
- pandas
- numpy
- nltk
- matplotlib
- gensim

Make sure to install all required libraries using `pip install -r requirements.txt` (if you have a `requirements.txt` file) 
or manually install them using `pip install <library>`.

## Usage

### Step 1: Calculate Dissimilarity Scores

Run the `dissimilarity_score.py` script first. It will process the user profiles to compute dissimilarity scores 
and save the results in a JSON file.

```sh
python dissimilarity_score.py
```

### Step 2: Identify Trusted Profiles

After calculating the dissimilarity scores, execute the `trusted_profile.py` script. It will use the scores 
from the first script to flag trusted profiles and save them for further analysis.

```sh
python trusted_profile.py
```

### Step 3: Distinguish Naive & Expert Profiles

Finally, use the `naive&expert.py` script to categorize the profiles into naive and expert groups. This script 
will also generate visualizations and save them to disk.

```sh
python naive&expert.py
```

## Output

The scripts will generate several output files, including:

- `dissimilarity_scores.json` - JSON file with dissimilarity scores.
- `trusted_profiles.csv` - CSV file listing trusted profiles.
- `naive_set.csv` and `expert_set.csv` - CSV files containing the segregated naive and expert profile sets.
- Various plots in PNG format visualizing the data analysis results.

## Notes

- Ensure that all scripts are in the same directory and that the input data files are correctly placed in this directory.
- If any changes are made to the filenames or paths within the scripts, update the README accordingly.
