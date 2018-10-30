# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import seaborn as sns
import time
plt.style.use('gadfly')
plot_kwds = {'alpha' : 0.25, 's' : 80, 'linewidths':0}

def plot_clusters(datax,datay,subplot, algorithm, args, kwds):
    start_time = time.time()
    data_pred = pd.DataFrame([datax,datay]).transpose()
    cnames = list(data_pred)
    labels = algorithm(*args, **kwds).fit_predict(data_pred)
    end_time = time.time()
    palette = sns.color_palette('deep', np.unique(labels).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
    plt.subplot(subplot)
    plt.scatter(datax, datay, c=colors, **plot_kwds)
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)
    plt.title('{} vs {} clusters'.format(cnames[0],cnames[1]), fontsize=10)
    print('Clustering took {:.2f} s'.format(end_time - start_time))
    return labels

# %%
FILEPATH = "C:/Users/jimta/Desktop/fc_secreted_degs.txt"
data = pd.read_csv(FILEPATH, names =['gene','6hr','12hr','15hr','24hr','36hr'])
full_data = data
data = data.drop(['gene'],axis=1)

plt.scatter(data['6hr'], data['12hr'], c='b', **plot_kwds)
frame = plt.gca()
frame.axes.get_xaxis().set_visible(True)
frame.axes.get_yaxis().set_visible(True)

# %%
comparisons = [['6hr','12hr'],['12hr','15hr'],['15hr','24hr'],['24hr','36hr']]
sp = 221
clusters_by_comparison = []
for comp in comparisons:
    x,y = comp
    label = plot_clusters(data[x],data[y],sp, DBSCAN,(),{'eps':.5})
    full_data['{}vs{}'.format(x,y)] = label
    groups = []
    for i in np.unique(label):
        g = [full_data['gene'][x] for x, v in enumerate(full_data['{}vs{}'.format(x,y)]) if v == i]
        groups.append(g)
    clusters_by_comparison.append(groups)
    sp = sp+1

# %%

group_df = pd.DataFrame(clusters_by_comparison)
group_df = group_df.transpose()
group_df.columns = ['6v12','12v15','15v24','24v36']

for comp in list(group_df):
    group_df[comp].to_csv('C:/Users/jimta/Desktop/{}_DBSCAN_groups_secretedonly.csv'.format(comp))
