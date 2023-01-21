import matplotlib.pyplot as plt
import glob
import os
import pandas as pd
import json
import src.MachineLearning.LocationAnalyzer as LA
import plotly.graph_objects as go

path = r'/Volumes/T7/auto diary/pythonProject/src/temp/InfoOfFiles.json'

with open(path) as json_file:
    json_data = json.load(json_file)


df = pd.DataFrame.from_dict(json_data).T

df_loc = df[['datetime', 'latitude', 'longitude']].dropna()
df_loc.index = pd.to_datetime(df_loc['datetime'])
df_loc['latitude'] = df_loc['latitude'].astype('float')
df_loc['longitude'] = df_loc['longitude'].astype('float')

df_loc = df_loc.query('latitude < 200 and longitude < 200')
df_loc = df_loc.sort_index()

print('aa')
#DB scan
locationClassifications = {}
df2, locationClassifications = LA.classifyLocations_DBSCAN(df_loc, locationClassifications)

LA.plotScatter(df2)



#MEANSHIFt
locationClassifications = {}
df2, locationClassifications_Meanshift = LA.classifyLocations_MeanShift(df_loc, locationClassifications, threshold = 1, )
print(locationClassifications_Meanshift)

print(df2[df2['classification'] == 0])
df2_classification0 = df2[df2['classification'] == 0]

print('aa')
locationClassifications2 = {}
df2_classification0, locationClassifications2 = LA.classifyLocations_MeanShift(df2_classification0, locationClassifications2)

fig, ax  = plt.subplots()

LA.plotScatter(df2)
LA.plotScatter(df2_classification0)




#plot on map
fig = go.Figure(go.Scattergeo())
go.Scatter(x = df_loc['latitude'], y = df_loc['longitude'], marker = dict(size = 20))
# fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
fig.add_trace(go.Scattergeo(lat = df_loc['latitude'].values, lon = df_loc['longitude'].values))
fig.show()

print(locationClassifications)