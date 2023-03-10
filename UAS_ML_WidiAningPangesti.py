# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NUmLtwvmFVNXZ_GFUFR1CU82LGJJZnNp
"""

# Load Library
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load Dataset
dt = pd.read_csv('/content/Liga120192021.csv')
x = dt.iloc[:,[8,9]].values

# menentukan range cluster
from sklearn.cluster import KMeans
x = dt.iloc[:,[8,9]].values

wcss = []
for i in range (1,11):
  kmeans = KMeans(n_clusters=i, init = 'k-means++', random_state = 32)
  kmeans.fit(x)
  wcss.append(kmeans.inertia_)

# menampilkan grafik dengan metode Elbow untuk menentukan range
plt.plot(range(1,11),wcss)
plt.title('Metode Elbow')
plt.xlabel('Jumlah clusters')
plt.ylabel('WCSS')
plt.show()

# Clustering 2 column dengan range = 3
kmeans = KMeans(n_clusters=3, init = 'k-means++', random_state = 32)
y_kmeans = kmeans.fit_predict(x)

plt.scatter(x[y_kmeans == 0, 0], x[y_kmeans == 0, 1], s=10, c='yellow', label='kluster 1')
plt.scatter(x[y_kmeans == 1, 0], x[y_kmeans == 1, 1], s=10, c='blue', label='kluster 2')
plt.scatter(x[y_kmeans == 2, 0], x[y_kmeans == 2, 1], s=10, c='green', label='kluster 3')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=100, c = 'red', label = 'Centroid')

plt.title('Cluster Assist Gol')
plt.xlabel('Pass 9')
plt.ylabel('Pass 10')
plt.legend()
plt.show()

# Library
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as pyplot
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import warnings
from scipy import stats
warnings.filterwarnings('ignore')

# Load Dataset
dt = pd.read_csv('/content/Liga120192021.csv')
dt

# Membuat function untuk membuat model KMeans
def createModelBy2Column(index):

  # Mengambil 2 Column berdasarkan index
  new_dt = dt[['Pass{0}'.format(index), 'Pass{0}'.format(index+1)]]
  scaler = StandardScaler()
  scaler.fit(new_dt)
  dt_scaled = scaler.transform(new_dt)
  dt_scaled = pd.DataFrame(dt_scaled)

  # Membuat Prediksi menggunakan K-Means
  km = KMeans(n_clusters=2)
  y_predicted = km.fit_predict(dt_scaled)

  # Mengatur ulang Columns
  new_dt.loc[:, "Cluster"] = y_predicted
  new_dt.loc[:, "Perpindahan"] = 'Pemain {0} - Pemain {1}'.format(index,index+1)
  new_dt.loc[:, "Passer"] = new_dt['Pass{0}'.format(index)]
  new_dt.loc[:, "Receiver"] = new_dt['Pass{0}'.format(index+1)]
  new_dt.drop(['Pass{0}'.format(index),'Pass{0}'.format(index+1)], axis=1)
  return new_dt

results = None

for key in range(len(dt.columns) -1):
  index = key + 1
  result = createModelBy2Column(index)
  if results is None:
    results = result
  else:
    results=pd.concat([results, result])

g = sns.FacetGrid(results, col='Perpindahan', hue = 'Cluster', height=5, col_wrap=3)
g.map(sns.scatterplot, 'Passer', 'Receiver')
g.add_legend()