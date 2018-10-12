# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


FILEPATH = "C:/Users/jimta/Documents/kmeans_data.csv"
data = pd.read_csv(FILEPATH, names =['gene','fungus12','maize12'])
data = data.drop(['gene'],axis=1)
kmeans = KMeans()
kmeans.fit(data)

labels = kmeans.predict(data)
centroids = kmeans.cluster_centers_


plt.subplot(121)
plt.scatter(data['fungus12'],data['maize12'])

X = [centroids[i][0] for i, j in enumerate(centroids)]

y = [centroids[i][1] for i, j in enumerate(centroids)]
plt.subplot(121)
plt.scatter(X,y,c='Orange')
for i in [0,1,2,3,4,5,6,7]:
    plt.annotate(i,(X[i],y[i]))

plt.show()
# %%
with open('kmeans_labels.txt', 'w') as file:
    for i in labels:
        file.writelines(str(i)+'\n')
