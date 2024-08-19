import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Read the CSV file
edges_df = pd.read_csv('b2b_transactions.csv')

# Create a graph from the DataFrame
G = nx.from_pandas_edgelist(edges_df, 'source', 'target', ['amount'])

# Compute the degree for each node
degrees = dict(G.degree())

# Normalize degree values for color mapping
norm = plt.Normalize(vmin=min(degrees.values()), vmax=max(degrees.values()))
cmap = plt.cm.viridis  # Using 'viridis' colormap for dark-to-light mapping

# Create a color array based on the degree of each node
node_colors = [cmap(norm(degrees[node])) for node in G.nodes()]

# Draw the graph
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.15, iterations=20)  # for better visual spacing

# Draw the nodes with colors based on degree
nx.draw_networkx_nodes(G, pos, node_size=10, node_color=node_colors, cmap=cmap)

# Draw the edges
nx.draw_networkx_edges(G, pos, alpha=0.3)

# Optionally, add a colorbar for reference
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
plt.colorbar(sm, label="Node Degree")

plt.title("B2B Transaction Network with Node Colors Based on Degree")
plt.show()
