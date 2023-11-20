import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

# Load the cleaned data
data = pd.read_csv('../dissimilarity/processed_data.csv', encoding='ISO-8859-1')

# Display the first few rows of the cleaned data
data.head()

# Drop the columns 'description', 'age', and 'scam'
data_to_cluster = data.drop(columns=['description', 'age', 'scam'])

# Convert categorical variables to numeric
le = LabelEncoder()
for column in data_to_cluster.columns:
    if data_to_cluster[column].dtype == "object":
        data_to_cluster[column] = le.fit_transform(data_to_cluster[column].astype(str))

# Scale the data for clustering
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data_to_cluster)

print(scaled_data[:5])

# Fitting the KMeans model with 6 clusters
kmeans = KMeans(n_clusters=6, random_state=0, n_init='auto')
data['cluster'] = kmeans.fit_predict(scaled_data)

# Group by cluster and compute scam counts
cluster_summary = data.groupby('cluster')['scam'].value_counts().unstack().fillna(0)

# Calculate total entries per cluster
cluster_summary['total'] = cluster_summary.sum(axis=1)

# Calculate the percentage of scams in each cluster
cluster_summary['scam_percentage'] = (cluster_summary[1] / cluster_summary['total']) * 100

# Keep only relevant columns
cluster_summary = cluster_summary[[1, 'scam_percentage']]
cluster_summary.columns = ['scam_count', 'scam_percentage']

print(cluster_summary)
