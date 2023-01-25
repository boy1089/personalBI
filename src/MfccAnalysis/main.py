import matplotlib.pyplot as plt

import pandas as pd
import os

path_average_std = r'/Volumes/T7/auto diary/dataAnalyzed/mfcc analysis/average, std.csv'
path_average_profile = r'/Volumes/T7/auto diary/dataAnalyzed/mfcc analysis/averageProfile.csv'
df = pd.read_csv(path_average_std)

df2 = df.copy()
df2.index = pd.to_datetime(df[df.columns[2]])
df2 = df2.sort_index()

for j in range(3):
    df3 = df2.between_time(f'{j*8}:00', f'{(j+1)*8 -1}:00')
    plt.scatter(df3['average'], df3['std'], s = 1, label = j)

plt.legend()
plt.xlim(-30, 0)
plt.ylim(40, 175)

print('aa')


df_profile = pd.read_csv(path_average_profile)
print(df_profile.columns)
df_profile.index = pd.to_datetime(df_profile[df_profile.columns[2]])
df_profile = df_profile.sort_index()

for j in [ 4, 5, 6, 7, 8]:
    plt.scatter(df_profile[df_profile.columns[3]], df_profile[df_profile.columns[j]], s = 1)

