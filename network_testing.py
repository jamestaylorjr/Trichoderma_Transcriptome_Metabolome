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
newsub = pd.read_csv('C:/Users/jimta/Desktop/6v12_DBSCAN_groups_effectoronly.csv', header=None)

newsub.head()


#
comparisons = ['6v12','12v15','15v24','24v36']
hub_genes = pd.DataFrame(index=range(10))
for x in comparisons:
    hub_holder = []
    newsub = pd.read_csv('C:/Users/jimta/Desktop/{}_DBSCAN_groups_effectoronly.csv'.format(x), header=None)
    for y in newsub:
        final_sub = [n for n in newsub[y] if n in nx.nodes(G)]
        connect = []
        for z in final_sub:
            btw = nx.betweenness_centrality_subset(G,[z],nx.nodes(G))
            m = statistics.mean(btw.values())
            connect.append(m)
        print(final_sub[connect.index(max(connect))],max(connect))
        hub_holder.append(final_sub[connect.index(max(connect))])
    df_holder = pd.DataFrame(hub_holder, columns=[x])
    hub_genes= hub_genes.join(df_holder)

print(hub_genes)
# %%
hub_genes.to_csv('C:/Users/jimta/Desktop/first_hubs.csv')
