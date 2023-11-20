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

# Determine the optimal number of clusters using the elbow method
inertia_values = []
cluster_range = range(1, 15)

for cluster_num in cluster_range:
    kmeans = KMeans(n_clusters=cluster_num, random_state=0, n_init='auto')
    kmeans.fit(scaled_data)
    inertia_values.append(kmeans.inertia_)

# Plotting the elbow curve
plt.figure(figsize=(10, 6))
plt.plot(cluster_range, inertia_values, marker='o', linestyle='--')
plt.title('Elbow Method for Optimal Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.grid(True)
plt.show()

# Cannot find the optimal number of clusters using the elbow method

silhouette_scores = []

# We'll check silhouette scores for a range of clusters (from 2 to 14 as silhouette score is not defined for 1 cluster)
for cluster_num in cluster_range[1:]:
    kmeans = KMeans(n_clusters=cluster_num, random_state=0, n_init='auto')
    cluster_labels = kmeans.fit_predict(scaled_data)
    silhouette_avg = silhouette_score(scaled_data, cluster_labels)
    silhouette_scores.append(silhouette_avg)

# Plotting the silhouette scores
plt.figure(figsize=(10, 6))
plt.plot(cluster_range[1:], silhouette_scores, marker='o', linestyle='--')
plt.title('Silhouette Method for Optimal Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.grid(True)
plt.show()

# Find out the optimal number of clusters is 6
