import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
edges_df = pd.read_csv('b2b_transactions.csv')

# Create a graph from the DataFrame
G = nx.from_pandas_edgelist(edges_df, 'source', 'target', ['amount'])

# Compute the degree for each node
degrees = [d for n, d in G.degree()]

# Plot the degree distribution
plt.figure(figsize=(10, 6))
plt.hist(degrees, bins=np.logspace(np.log10(min(degrees)), np.log10(max(degrees)), 50), density=True)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Degree (k)')
plt.ylabel('P(k)')
plt.title('Degree Distribution with Power-Law Fit')

# Fit a power-law to the degree distribution
from scipy.stats import powerlaw

# We will fit a power law to the data to confirm
fit_alpha, loc, scale = powerlaw.fit(degrees, floc=0, fscale=1)

# Plot the power-law fit
x = np.linspace(min(degrees), max(degrees), 100)
plt.plot(x, powerlaw.pdf(x, fit_alpha, loc=loc, scale=scale), 'r--', linewidth=2, label=f'Power-law fit: alpha={fit_alpha:.2f}')

plt.legend()
plt.show()
