import json
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from tqdm import tqdm
from gensim.models import Word2Vec
from scipy.stats import pearsonr

# Initialize NLTK components and progress bar for Pandas
nltk.download('punkt')
tqdm.pandas()

# Metadata attributes
union_meta = ['scam', 'username', 'age', 'gender', 'location', 'ethnicity', 'occupation', 
              'marital_status', 'children', 'religion', 'sexual_orientation', 'sex', 'description']
scam_meta = ['email']

# Load and preprocess the profile data
all_profile = pd.read_csv('processed_data.csv')
all_profile = all_profile.dropna(subset=['description'])
all_profile['tokenized'] = all_profile['description'].progress_apply(word_tokenize)

# Define a function to pad sequences to a maximum length
def pad_sequence(seq, max_len=100, padding_token='<PAD>'):
    return seq[:max_len] + [padding_token] * (max_len - len(seq))

# Apply padding to the tokenized descriptions
all_profile['padded'] = all_profile['tokenized'].apply(pad_sequence, max_len=100)

# Train the w2v model and save for future use
# w2v_model = Word2Vec(sentences=all_profile['tokenized'], vector_size=100, window=5, min_count=1, workers=4)
# w2v_model.save("word2vec_model.bin")

# Load a pre-trained Word2Vec model
w2v_model = Word2Vec.load("word2vec_model.bin")

# Function to transform tokens into vectors using the Word2Vec model
def tokens_to_vectors(tokens, model):
    vectors = [model.wv[token] for token in tokens if token in model.wv]
    return np.mean(vectors, axis=0) if vectors else np.zeros((100, model.vector_size))

# Convert the padded tokens into vectors
all_profile['vectors'] = all_profile['padded'].apply(tokens_to_vectors, model=w2v_model)

# Save the all_profile DataFrame to a CSV file
all_profile.to_csv('all_profile.csv')

# Separate the scammer and normal profiles
scammer_profiles = all_profile[all_profile['scam'] == 1]
normal_profiles = all_profile[all_profile['scam'] == 0]

# Initialize a dictionary to store Pearson Correlation Coefficients (PCC) results
pcc_results = {}

# Compare scammer profiles against normal profiles to find similarities
for scam_index, scam_row in scammer_profiles.iterrows():
    scammer_vector = scam_row['vectors']
    scores = []
    for normal_index, normal_row in normal_profiles.iterrows():
        normal_vector = normal_row['vectors']
        if len(scammer_vector) == len(normal_vector):
            corr, _ = pearsonr(scammer_vector, normal_vector)
            scores.append((normal_index, corr))
    scores.sort(key=lambda x: x[1], reverse=True)
    pcc_results[scam_index] = scores[:10]

# Convert PCC results to a JSON-compatible format
pcc_results_json = json.dumps({str(key): value for key, value in pcc_results.items()})

# Save the PCC results to a JSON file
with open('pcc_results.json', 'w') as file:
    file.write(pcc_results_json)