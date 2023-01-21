


import os
import json
import pandas as pd
import matplotlib.pyplot as plt
path = r"/Volumes/T7/auto diary/pythonProject/src/test/InfoOfFiles.json"


from sklearn.preprocessing import scale
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
import numpy as np

# with open(path, 'r') as json_file:
#     json.dump(data, json_file)

def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices

print('a')

with open(path, 'r') as json_file:
    data = json.load(json_file)

print(data.keys())

df = pd.read_json(path).T
df = df[df['latitude'] < 300]
df = df[df['longitude'] < 300]
df['latitude'] = [np.log(x) for x in df['latitude']]
df['longitude'] = [np.log(x) for x in df['longitude']]

# plt.figure()
# plt.plot(df['latitude'].values)
# plt.plot(df['longitude'].values)



df_temp = df[['latitude', 'longitude']].fillna(0)
kmeans = KMeans(n_clusters = 20, init = 'k-means++', max_iter = 300, random_state = 0)
kmeans.fit(df_temp)

setOfClassification = list(set(kmeans.labels_))
for i, classification in enumerate(setOfClassification):
    index = find_indices(kmeans.labels_, classification)
    plt.scatter(df_temp['longitude'][index],df_temp['latitude'][index] , label = index, s = 1)

# plt.ylim(30, 45)
# plt.xlim(120, 135)


