# Data Clustering and Analysis

This repository contains scripts for performing clustering analysis on a dataset. The primary focus is to identify optimal clusters within the data and analyze the characteristics of these clusters, particularly in terms of scam identification.

## Overview

The script performs the following key operations:

1. **Data Loading and Preprocessing:** Loads a cleaned dataset and preprocesses it by dropping specific columns and converting categorical variables to numeric.

2. **Data Scaling:** Standardizes the features for effective clustering.

3. **Clustering Analysis:** 
    - Implements the KMeans algorithm.
    - Uses the Elbow Method and Silhouette Scores to determine the optimal number of clusters.
    - Assigns each data point to a cluster.

4. **Cluster Analysis:** Analyzes each cluster, particularly focusing on the prevalence of scams within each cluster.

## Requirements

- pandas
- scikit-learn
- matplotlib

## Usage

1. **Load and Clean the Data:** Data is loaded from a CSV file, and specific columns are dropped. Categorical variables are converted to numeric.

2. **Scale the Data:** The data is scaled using `StandardScaler` to ensure uniformity in variance and mean.

3. **Determine Optimal Clusters:**
    - The Elbow Method is used to visualize the inertia across different cluster counts.
    - The Silhouette Method is used to analyze the cohesion and separation of clusters.

4. **Cluster Assignment:** The KMeans model is fitted with the optimal number of clusters determined, and each data point is assigned to a cluster.

5. **Cluster Summary:** Each cluster is analyzed for the count and percentage of scams, providing insights into the characteristics of each cluster.

## Results

- The optimal number of clusters is determined based on Elbow and Silhouette methods.
- The final output includes a summary of each cluster, focusing on the prevalence of scams.
