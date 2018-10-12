import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

filename = "C:/Users/jimta/Desktop/DGE_NoRNA.txt"

network = pd.read_table(filename, sep='\t', names = ['Source','Destination','Weight'])
print(len(network['Source']))

# %%
G = nx.Graph()
for i, gene in enumerate(network['Source'][:100000]):
    G.add_edge(network['Source'][i],network['Destination'][i],weights=network['Weight'][i])
G.number_of_nodes()

# %%
betwn = nx.betweenness_centrality(G)
print(min(betwn))
# %%
nx.draw(G)
