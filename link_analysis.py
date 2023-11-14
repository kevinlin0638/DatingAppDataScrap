import networkx as nx
import pandas as pd
# Perform Community Detection using the Louvain method
import community as community_louvain

# Load the data from the CSV file
file_path = './normal/user_friends.csv'
user_friends_data = pd.read_csv(file_path)

# Display the first few rows of the dataframe to understand its structure
print(user_friends_data.head())

# Create a directed graph from the dataframe
graph = nx.from_pandas_edgelist(user_friends_data, 'username', 'friend_username', create_using=nx.DiGraph())

# Compute the PageRank of the graph
pagerank_scores = nx.pagerank(graph)

# Convert the PageRank scores to a dataframe for better visualization
pagerank_df = pd.DataFrame(list(pagerank_scores.items()), columns=['User', 'PageRank Score']).sort_values(by='PageRank Score', ascending=False)

print(pagerank_df.head())  # Display the top users by PageRank score
pagerank_df.to_csv('pagerank.csv', index=False)

# Calculate Betweenness Centrality for the users
betweenness_centrality = nx.betweenness_centrality(graph)

# Convert the Betweenness Centrality scores to a dataframe
betweenness_df = pd.DataFrame(list(betweenness_centrality.items()), columns=['User', 'Betweenness Centrality']).sort_values(by='Betweenness Centrality', ascending=False)

# The Louvain method works on undirected graphs, so we convert our graph to undirected for this analysis
communities = community_louvain.best_partition(graph.to_undirected())

# Add the community info to the betweenness dataframe
betweenness_df['Community'] = betweenness_df['User'].map(communities)

# Show the top users by Betweenness Centrality
top_betweenness = betweenness_df.head()

# Find out how many communities have been detected
num_communities = len(set(communities.values()))
print(top_betweenness)
print(num_communities)
betweenness_df.to_csv('top_betweenness.csv', index=False)


# ----------------------------------------------------------------

# Count the number of users in each community
community_counts = pd.Series(communities).value_counts()

# Identify the top 5 communities
top_5_communities = community_counts.head(5).index

# Gather users in the top 5 communities
top_communities_users = {community: [] for community in top_5_communities}
for user, community in communities.items():
    if community in top_5_communities:
        top_communities_users[community].append(user)

# Print the sizes of the top 5 communities
print("Top 5 Communities by Size:")
for community in top_5_communities:
    print(f"Community {community}: {len(top_communities_users[community])} members")

# Print the members of each top community
# for community, users in top_communities_users.items():
#     print(f"\nUsers in Community {community}:")
#     print(users)
