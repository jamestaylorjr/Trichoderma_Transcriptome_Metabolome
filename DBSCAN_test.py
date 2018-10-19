# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import seaborn as sns
import time
plt.style.use('gadfly')
plot_kwds = {'alpha' : 0.25, 's' : 80, 'linewidths':0}

def plot_clusters(data, algorithm, args, kwds):
    start_time = time.time()
    labels = algorithm(*args, **kwds).fit_predict(data)
    end_time = time.time()
    palette = sns.color_palette('deep', np.unique(labels).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
    plt.scatter(data['6hr'], data['12hr'], c=colors, **plot_kwds)
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)
    plt.title('Clusters found by {}'.format(str(algorithm.__name__)), fontsize=10)
    print('Clustering took {:.2f} s'.format(end_time - start_time))
    return labels

# %%
FILEPATH = "C:/Users/jimta/Desktop/fc_degs.txt"
data = pd.read_csv(FILEPATH, names =['gene','6hr','12hr'])
full_data = data
data = data.drop(['gene'],axis=1)

plt.scatter(data['6hr'], data['12hr'], c='b', **plot_kwds)
frame = plt.gca()
frame.axes.get_xaxis().set_visible(True)
frame.axes.get_yaxis().set_visible(True)

# %%
label = plot_clusters(data, DBSCAN, (), {'eps':0.37})
full_data['group'] = label

# %%
groups = []
for i in np.unique(label):
    g = [full_data['gene'][x] for x, v in enumerate(full_data['group']) if v == i]
    groups.append(g)

# %%
group_df = pd.DataFrame(groups)
group_df = group_df.transpose()
group_df.to_csv('C:/Users/jimta/Desktop/DBSCAN_groups_effectoronly.csv')
