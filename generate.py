import numpy as np
import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd

# Parameters for power-law distribution
alpha = 2.5
x_min = 3
amount_min = 100
amount_max = 10000
n_nodes = 100000  # number of nodes
csv_file = 'b2b_transactions_n100000.csv'

# Generate degrees for each node using a power-law distribution
degrees = np.random.zipf(alpha, n_nodes)

# Ensure all nodes have a degree of at least 3
for i in range(len(degrees)):
    if degrees[i] < x_min:
        degrees[i] = x_min

# Ensure that the degrees sum to an even number (required for a valid graph)
if sum(degrees) % 2 != 0:
    degrees[random.randint(0, len(degrees) - 1)] += 1

# Generate a configuration model graph
G = nx.configuration_model(degrees)

# Convert to a simple graph (remove multi-edges and self-loops)
G = nx.Graph(G)  # Convert to simple graph
G.remove_edges_from(nx.selfloop_edges(G))

# Check if any node still has a degree less than x_min after conversion
while any(d < x_min for _, d in G.degree()):
    # Find nodes with degree less than x_min
    low_degree_nodes = [node for node, degree in G.degree() if degree < x_min]
    
    for node in low_degree_nodes:
        # Randomly select another node to connect with, ensuring no self-loops
        possible_targets = [n for n in G.nodes if n != node and not G.has_edge(node, n)]
        if possible_targets:
            target = random.choice(possible_targets)
            G.add_edge(node, target)

# Assign random transaction amounts to each edge
amounts = [random.randint(amount_min, amount_max) for _ in range(len(G.edges))]

for (u, v), amount in zip(G.edges(), amounts):
    G[u][v]['amount'] = amount

edges_df = pd.DataFrame([(u, v, G[u][v]['amount']) for u, v in G.edges()],
                        columns=['source', 'target', 'amount'])

# Display the DataFrame
edges_df.head()

# Optional: Save the DataFrame to a CSV file
edges_df.to_csv(csv_file, index=False)

# Optional: Plot the degree distribution to check
degrees = [d for n, d in G.degree()]
plt.hist(degrees, bins=range(1, max(degrees) + 2))
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Degree')
plt.ylabel('Frequency')
plt.title('Degree distribution of B2B transaction network')
plt.show()
