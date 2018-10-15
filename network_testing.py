import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import statistics

filename = "C:/Users/jimta/Desktop/DGE_final_geneNet.tab"

network = pd.read_table(filename, sep='\t', names = ['Source','Destination','Weight'])
print(len(network['Source']))

# %%
G = nx.Graph()
for i, gene in enumerate(network['Source']):
    G.add_edge(network['Source'][i],network['Destination'][i],weights=network['Weight'][i])
G.number_of_nodes()

# %%
#betwn = nx.betweenness_centrality(G)
with open('C:/Users/jimta/Desktop/group_test.tab','r') as file:
    sub = file.readlines()

newsub = [s.strip('\n') for s in sub]

final_sub = [n for n in newsub if n in nx.nodes(G)]

# %%
connect = []
for x in final_sub:
    btw = nx.betweenness_centrality_subset(G,[x],nx.nodes(G))
    m = statistics.mean(btw.values())
    connect.append(m)
print(final_sub[connect.index(sorted(connect,reverse=True)[2])])
print(final_sub[connect.index(max(connect))],max(connect))

# %% Don't run this cell. It takes forever for very little payoff.
#nx.draw(G)
