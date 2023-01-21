import os

import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt

import matplotlib
from matplotlib import rc, font_manager
import datetime as datetime

rc('font',family='AppleGothic')
# matplotlib.use('TkAgg')

pathOfGoogleDrive = r"/Users/jiyoung/Library/CloudStorage/GoogleDrive-boytoboy0108@gmail.com/내 드라이브/autodiary data"
pathOfSensorData = pathOfGoogleDrive + r"/sensorData"
pathOfActivityWatchData = pathOfGoogleDrive + r"/usageData"


def parseData(df):
    df_new = pd.DataFrame()
    columns = df.columns
    df_new['longitude'] = df[columns[1]]
    df_new['latitude'] = df[columns[2]]
    df_new = df_new.astype('float')
    # print(pd.to_datetime(df['time']))
    df_new.index = pd.to_datetime(df['time'])
    df_new =df_new[1:]
    return df_new

def readSensorData(length =  14):
    files = glob.glob(f"{pathOfSensorData}/*.csv")
    files.sort(reverse = True)
    dataList = []
    for i, file in enumerate(files[:length]):
        df = pd.read_csv(file, sep = ",")
        df2 = parseData(df)
        dataList.append(df2)
    return dataList

def readActivityWatchData(length = 30000):
    files = glob.glob(f"{pathOfActivityWatchData}/*.json")
    files.sort()

    dataDic = {}
    for i, file in enumerate(files):
        print(i, file)
        df = pd.read_json(file)
        client = df['buckets'].values[0]['client']
        #list of data : name of app running
        # result, listOfData = parseActivityWatchData(df)
        df = parseActivityWatchData(df, length = length)
        dataDic[client] = df

    return dataDic

def parseActivityWatchData(df, length = 10000):
    events = df['buckets'].values[0]['events']
    client = df['buckets'].values[0]['client']
    df = pd.DataFrame(columns=list(events[0].keys()))

    for i, event in enumerate(events[:length]):
        values = list(event.values())
        print(values)
        df_event = pd.DataFrame(values[:len(values) - 1] + [values[len(values) - 1]['app']]).T
        df_event.columns = list(event.keys())
        df = pd.concat([df, df_event], axis=0)

    listOfData = list((set(df['data'].to_list())))

    df['dataIndex'] = [listOfData.index(x) for x in df['data']]
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')

    # list2 = []
    # for i, index in enumerate(listOfData):
    #     df2 = df[df['dataIndex'] == i]
    #     list2.append(df2.index.values)
    # return list2, listOfData

    return df

# arrange data for one day
def calculateTimeSpentForOneDay(df, date, index = 0):
    keys = list(df.keys())
    df_temp = df[keys[index]][date]
    listOfData = list(set(df_temp['data'].values))
    listOfData = [x for x in listOfData if x.find('ScreenSaver') ==-1]

    df_timeSpent = pd.DataFrame()

    for i, dataType in enumerate(listOfData):
        df_temp2 = df_temp[df_temp['data'] == dataType]
        timeSpent = df_temp2['duration'].sum()
        df_timeSpent = pd.concat([df_timeSpent, pd.Series([dataType, timeSpent]).T], axis = 1)

    df_timeSpent = df_timeSpent.T
    print(df_timeSpent)

    df_timeSpent.columns = ['app', 'timeSpent']
    df_timeSpent = df_timeSpent.sort_values('timeSpent')
    df_temp3 = pd.DataFrame(['not using', 24*60*60 - df_timeSpent['timeSpent'].sum()]).T
    df_temp3.columns = ['app', 'timeSpent']
    df_timeSpent = pd.concat([df_timeSpent, df_temp3])

    return df_timeSpent


#input
base = datetime.datetime(2023, 1, 8)
base = datetime.datetime(2022, 12, 25)
index = 0
dateRange = 14


data = readActivityWatchData()


dates = [(base - datetime.timedelta(days=x)).date().strftime('%Y-%m-%d') for x in range(dateRange)]
dates.sort()

listOfDf_timespent = []

df_timeSpentOfDates = pd.DataFrame()
print(len(data[list(data.keys())[0]]['2022-12-16']))

for i, date in enumerate(dates):
    if(len(data[list(data.keys())[index]][date]) ==0):
        dates.remove(date)
        continue
    df_timeSpentOfDate = calculateTimeSpentForOneDay(data, date, index = index)
    df_timeSpentOfDate.columns = ['app', f'timeSpent_{date}']
    df_timeSpentOfDate = df_timeSpentOfDate.set_index('app')
    df_timeSpentOfDates = pd.concat([df_timeSpentOfDates, df_timeSpentOfDate], axis = 1)

apps = df_timeSpentOfDates.index
# apps = [x for x in apps if x.find('ScreenSaver') ==-1]
print(df_timeSpentOfDates.columns)

fig, ax = plt.subplots(figsize = (50, 20))
bottoms = np.zeros(len(dates))

print(df_timeSpentOfDates)
print(apps)
for i, app in enumerate(apps):
    timeSpentForApp = df_timeSpentOfDates.loc[app].fillna(0) / 60 / 60
    ax.bar(dates, timeSpentForApp.values, label = app, bottom = list(bottoms))
    bottoms = bottoms + np.asarray(timeSpentForApp)

    if((timeSpentForApp[0] > 1000 / 60 / 60)| (timeSpentForApp[5] > 1000 / 60 / 60)):
        for j in range(len(bottoms)):
            text = f"{app}, {timeSpentForApp[j]:.1f} hours"
            plt.text(j - 0.5, bottoms[j] - timeSpentForApp[j] / 2, text)

ax.set_ylabel('time spent [hr]')

