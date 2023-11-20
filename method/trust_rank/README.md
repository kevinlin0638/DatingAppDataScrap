# Trust Score Computation and Profile Similarity Analysis in Social Networks

This repository contains scripts for computing trust scores and analyzing profile similarity in a social network using network graph metrics. The analysis involves reading user data, building a graph of connections, and applying the PageRank algorithm to determine trust scores.

## Overview

The scripts perform the following key operations:

1. **Initial Data Setup:**
    - Reads trusted user profiles and user friendships data from CSV files.
    - Creates a set of trusted usernames and constructs a social graph based on user connections.

2. **Trust Score Computation:**
    - Initializes trust scores, assigning higher initial scores to trusted users.
    - Applies the PageRank algorithm with a damping factor to propagate trust scores through the network.

3. **Profile Similarity Analysis:**
    - Merges trust scores with user profile data to analyze profile similarities.
    - Exports the results to CSV files for further analysis.

4. **Trust Score Reset and Recomputation:**
    - Resets trust scores based on a subset of users identified by initial PageRank.
    - Recomputes trust scores using the new initial values.

## Requirements

- pandas
- networkx

## Usage

1. **Data Preparation:** The script reads user profile data and friendship connections from CSV files and creates a network graph.

2. **Initial Trust Score Computation:** The PageRank algorithm is used to compute initial trust scores based on the network graph and a set of trusted user profiles.

3. **Trust Rank and Profile Similarity Analysis:** The trust scores are merged with user profile data to analyze the similarity between profiles, and the results are saved to a CSV file.

4. **Trust Score Reset and Recomputation:** Trust scores are reset based on a selected subset of users and recomputed using the PageRank algorithm.

## Results

- The scripts produce trust scores for users in the network, which are indicative of their reliability or importance within the network based on connections.
- The analysis provides insights into profile similarities and trust dynamics within the social network.
