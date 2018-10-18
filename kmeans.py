# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
plt.style.use('gadfly')
# %%
# this cell from https://github.com/joaofig/auto-k-means
import math


class KEstimator:
    """
    Riddle K-estimator.
    Estimates the correct value for K using the reciprocal delta log rule.
    """
    def __init__(self, cluster_fn=None):
        self.K = 0
        self.cluster = cluster_fn
        self.s_k = dict()

    def fit(self, X, max_k=50):
        r_k = dict()
        max_val = float('-inf')

        for k in range(1, max_k + 1):
            self.s_k[k] = self.cluster(X, k)
            r_k[k] = 1.0 / self.s_k[k]

            if k > 1:
                d = (r_k[k] - r_k[k-1]) / math.log(k)
                if d > max_val:
                    max_val = d
                    self.K = k
        return self.K

    def fit_s_k(self, s_k, max_k=50):
        """Fits the value of K using the s_k series"""
        r_k = dict()
        max_val = float('-inf')

        for k in range(1, max_k + 1):
            r_k[k] = 1.0 / s_k[k]

            if k > 1:
                d = (r_k[k] - r_k[k-1]) / math.log(k)
                if d > max_val:
                    max_val = d
                    self.K = k
        self.s_k = s_k
        return self


# %%

FILEPATH = "C:/Users/jimta/Desktop/potential_targets.txt"
data = pd.read_csv(FILEPATH, names =['gene','fungus','maize'])
full_data = data
data = data.drop(['gene'],axis=1)

# %% Estimate optimal number of clusters for KMeans
s_k = []

for k in range(1,len(data)-1):
    km = KMeans(n_clusters=k).fit(data)
    s_k.append(km.inertia_)

riddle_estimator = KEstimator()

riddle_estimator.fit_s_k(s_k, max_k=40)
print('riddle : {0}'.format(riddle_estimator.K))

m_k = riddle_estimator.K

# %%
#kmeans = KMeans(n_clusters=m_k)
kmeans = KMeans()
kmeans.fit(data)

labels = kmeans.predict(data)
centroids = kmeans.cluster_centers_


plt.subplot(121)
plt.scatter(data['fungus'],data['maize'])

X = [centroids[i][0] for i, j in enumerate(centroids)]

y = [centroids[i][1] for i, j in enumerate(centroids)]
plt.subplot(121)
plt.scatter(X,y,c='Orange')
'''
for i in range(0,m_k-1):
    plt.annotate(i,(X[i],y[i]))
'''
plt.show()

# %%
with open('kmeans_label.txt', 'w') as file:
    for i in labels:
        file.writelines(str(i)+'\n')

# %%
full_data['group'] = labels
full_data = full_data.drop(['fungus'], axis=1)
full_data = full_data.drop(['maize'],axis = 1)

# %%
g_names = []
for x in range(max(labels)):
    g_names.append("g{}".format(x))

groups = pd.DataFrame(columns=g_names)

# %%
for i, g in enumerate(full_data['group']):
    groups = groups.append({'g{}'.format(g) : full_data['gene'][i]},ignore_index=True)

# %%
group_list= [list(groups[g].dropna()) for g in groups]

# %%
with open('list_of_groups_2.txt','w') as output:
    for i in group_list:
        output.writelines(str(i)+'\n')
