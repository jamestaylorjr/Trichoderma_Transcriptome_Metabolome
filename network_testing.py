import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

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
newsub = []
for s in sub:
    newsub.append(s.strip('\n'))

final_sub = []
for n in nx.nodes(G):
    if n in newsub:
        final_sub.append(n)

betwn = nx.betweenness_centrality_subset(G,final_sub,final_sub)
# %%
top5 = sorted(betwn,key=betwn.get,reverse=True)
print(top5[:4])
print(max(betwn, key=betwn.get))
print(betwn[max(betwn, key=betwn.get)])

# %%
nx.draw(G)
