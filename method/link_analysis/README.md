# Social Network Analysis of User Friendships

This repository contains scripts for analyzing a social network of user friendships. The analysis includes calculating graph metrics like PageRank and Betweenness Centrality, and detecting communities using the Louvain method.

## Overview

The scripts perform the following key operations:

1. **Data Loading and Graph Creation:**
    - Loads user friendship data from a CSV file.
    - Creates a directed graph representing user connections.

2. **Graph Metrics Computation:**
    - Calculates PageRank scores for users.
    - Computes Betweenness Centrality for each user.

3. **Community Detection:**
    - Applies the Louvain method for community detection in the network.
    - Assigns community labels to users based on their connections.

4. **Analysis and Reporting:**
    - Identifies and reports on the top communities by size and the significance of users within these communities.
    - Calculates and compares the PageRank scores within and across different communities.

## Requirements

- pandas
- networkx
- community (python-louvain)

## Usage

1. **Data Preparation:** The CSV file containing user friendships is loaded and used to create a directed graph.

2. **PageRank Calculation:** The PageRank algorithm is applied to the graph to identify influential users.

3. **Betweenness Centrality Calculation:** Betweenness Centrality is computed to find users who serve as bridges in the network.

4. **Community Detection:** The Louvain method is used on the undirected version of the graph to detect communities.

5. **Analysis of Communities:** Communities are analyzed based on their size, and the significance of users is evaluated based on their PageRank scores and community membership.

## Results

- The analysis results in a set of metrics (PageRank, Betweenness Centrality) for each user.
- Communities within the network are identified, and key users within these communities are highlighted.
- The script provides insights into the structure and dynamics of the social network.
