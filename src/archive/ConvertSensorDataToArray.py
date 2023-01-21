import pandas as pd
import os
import datetime

path = r"/Volumes/T7/auto diary/pythonProject/data/sensor/20220823_sensor.csv"
import numpy as np
df = pd.read_csv(path)
df['time'] = pd.to_datetime(df['time'])
print(df['time'])
df['time_temp'] = [datetime.datetime.combine(datetime.date(1970, 1, 1), x.time()) for x in df['time']]
df['theta'] = df['time_temp'].values.astype(int) / 1e9 / 3600 / 24 * 2 * np.pi
path_save = r"/Volumes/T7/auto diary/pythonProject/data"

print(df.columns)
df = df[['theta', ' longitude', ' latitude', ' accelX', ' accelY', ' accelZ ']]
# df.columns = [x.strip() for x in df.columns.values]

# file = open(os.path.join(path_save, 'array.txt'), 'w')
# line = df.columns.values.tolist()
# file.write('[')
# file.write(
#     f'["{line[0]}", "{line[1]}", "{line[2]}", "{line[3]}", "{line[4]}", "{line[5]}"], \n'
# )
#
# for j, line in enumerate(df.loc):
#     file.write(
#         f'[{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[4]}, {line[5]}], \n'
#     )
# print(len(df))
# file.write(']')

print(df.columns)
df = df[['theta', ' longitude', ' latitude', ' accelX', ' accelY', ' accelZ ']]
df.columns = [x.strip() for x in df.columns.values]

file = open(os.path.join(path_save, 'array.txt'), 'w')
line = df.columns.values.tolist()
file.write('[')
file.write(
    f'["{line[0]}", "{line[1]}", "{line[2]}", "{line[3]}", "{line[5]}"], \n'
)

for j, line in enumerate(df.loc):
    file.write(
        f'[{line[0]}, {line[1]}, {line[2]}, {line[3]}, {line[5]}], \n'
    )
print(len(df))
file.write(']')