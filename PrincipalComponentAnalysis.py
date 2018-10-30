import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
plt.style.use('gadfly')



filepath = 'C:/Users/jimta/Desktop/DEG_counts_csv.csv'
df = pd.read_csv(filepath, names = ['target','fungus12_1','fungus12_2','fungus12_3','fungus15_1','fungus15_2','fungus15_3','fungus24_1','fungus24_2','fungus24_3','fungus36_1','fungus36_2','fungus36_3','fungus6_1','fungus6_2','fungus6_3','fungus_and_maize_12_1','fungus_and_maize_12_2','fungus_and_maize_12_3','fungus_and_maize_15_1','fungus_and_maize_15_2','fungus_and_maize_15_3','fungus_and_maize_24_1','fungus_and_maize_24_2','fungus_and_maize_24_3','fungus_and_maize_36_1','fungus_and_maize_36_2',	'fungus_and_maize_36_3','fungus_and_maize_6_1','fungus_and_maize_6_2','fungus_and_maize_6_3'])

df.head()

features = ['fungus12_1','fungus12_2','fungus12_3','fungus15_1','fungus15_2','fungus15_3','fungus24_1','fungus24_2','fungus24_3','fungus36_1','fungus36_2','fungus36_3','fungus6_1','fungus6_2','fungus6_3','fungus_and_maize_12_1','fungus_and_maize_12_2','fungus_and_maize_12_3','fungus_and_maize_15_1','fungus_and_maize_15_2','fungus_and_maize_15_3','fungus_and_maize_24_1','fungus_and_maize_24_2','fungus_and_maize_24_3','fungus_and_maize_36_1','fungus_and_maize_36_2',	'fungus_and_maize_36_3','fungus_and_maize_6_1','fungus_and_maize_6_2','fungus_and_maize_6_3']

x = df.loc[:, features].values
x2 = df.loc[:, features].values
y = df.loc[:,['target']].values
x = StandardScaler().fit_transform(x)

pca = PCA(n_components=2)

principalComponents = pca.fit_transform(x)

principalDF = pd.DataFrame(data=principalComponents, columns = ['principal component 1','principal component 2'])

finalDf = pd.concat([principalDF,df[['target']]],axis=1)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.set_title('2 component PCA')

ax.scatter(finalDf['principal component 1'],finalDf['principal component 2'])

ax.grid()


# %%

pca2 = PCA(.99)

pca.fit(x2)

pca.n_components_
