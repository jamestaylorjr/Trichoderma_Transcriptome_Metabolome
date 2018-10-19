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
'''
with open('C:/Users/jimta/Desktop/potential_targets_effectorsonly.txt','r') as file:
    sub = file.readlines()

newsub = [s.strip('\n') for s in sub]
'''
newsub = pd.read_csv('C:/Users/jimta/Desktop/DBSCAN_groups_effectoronly.csv')

newsub.head()
newsub = newsub.drop(newsub.columns[0],axis=1)

# %%
for x in newsub:
    final_sub = [n for n in newsub[x] if n in nx.nodes(G)]
    connect = []
    for z in final_sub:
        btw = nx.betweenness_centrality_subset(G,[z],nx.nodes(G))
        m = statistics.mean(btw.values())
        connect.append(m)
    print(final_sub[connect.index(max(connect))],max(connect))

# %% Don't run this cell. It takes forever for very little payoff.
#nx.draw(G)
print(connect[final_sub.index("TRIVIDRAFT_18067")])
