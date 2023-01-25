from src.DataManager import DataLoader
import matplotlib.pyplot as plt
import pandas as pd
import util as util
import datetime
import calmap
from matplotlib import rc
import MachineLearning.AnomalyDetector as AD
import MachineLearning.LocationAnalyzer as LA
import numpy.random as random

rc('font',family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


home_latitude = 37.3611
home_longitude = 126.7187


def checkIsHome(df, home_latitude, home_longitude, threshold = 1):
    distanceList = []
    longList = df['longitude'].values
    latList = df['latitude'].values
    for j in range(len(longList)):
        distance = util.calculateDistance(home_latitude, home_longitude, latList[j], longList[j])
        distanceList.append(distance)

    df['distanceToHome'] = distanceList
    df['isHome'] = df['distanceToHome'] < threshold
    return df

def getUsageData(df):
    return df[['link', 'type', 'note']].dropna().sort_index()

def getOneDayData(df, date, removeDate = False):
    df_oneDay = df[['link', 'type', 'note']].loc[date].dropna().sort_index()
    if(removeDate):
        df_oneDay.index = df_oneDay.index.time
        df_oneDay.index = [x.hour + x.minute/60 + x.second/3600 for x in df_oneDay.index.values]
    return df_oneDay

def plotUsageData(df, ax = None, offset = 0, setOfType = None):
    if setOfType == None :
        setOfType = util.getSetOfItem(df['type'])

    print(f"setOfType : {util.getSetOfItem(df['type'])}")
    if ax == None :
        fig, ax = plt.subplots()
    for j in range(len(setOfType)):
        try :
            ax.eventplot([df[df['type'] == setOfType[j]].index], label=setOfType[j], colors=util.colors[j], lineoffsets = offset)
        except :
            print(f'error, {j}')
            pass

    return ax

def convertStringIndexToDatetimeIndex(df):
    df.index = pd.to_datetime(df.index)
    return df


def calculateCountsOfDF(df, dateRange = util.getDates(datetime.datetime(2022, 8, 30), 240), column = 'type', ):
    setOfType = util.getSetOfItem(df[column].dropna())
    df_typeCounts = pd.DataFrame(index = setOfType)
    for i, date in enumerate(dateRange):
        df_oneDay = getOneDayData(df, date)
        typeCounts = df_oneDay[column].value_counts()
        df_typeCounts[date] = typeCounts
    df_typeCounts = df_typeCounts.T
    df_typeCounts.fillna(0)

    df_typeCounts = convertStringIndexToDatetimeIndex(df_typeCounts)
    df_typeCounts = df_typeCounts.fillna(0)
    sum = df_typeCounts.sum()
    df_typeCounts = df_typeCounts[sum.sort_values(ascending=False).index]

    return df_typeCounts


def yearplotCounts(df):
    fig, ax = plt.subplots(1, len(df.columns), figsize = (50, 20))
    for index in range(len(df.columns)):
        column = df.columns[index]
        ax[index] = calmap.yearplot(df[column], ax=ax[index], daylabels='MTWTFSS', monthticks=3)
        ax[index][0].set_title(column)


def calculateCounts(dates, df_usage):
    counts = pd.DataFrame()
    for i, date in enumerate(dates):
        print(f'calculating counts...{i}')
        df_oneDay = getOneDayData(df_usage, date, removeDate=True)
        # df_oneDay = df_oneDay[df_oneDay['type'] == '검색']
        # ax = plotUsageData(df_oneDay, ax, offset = i, setOfType = setOfType)
        df_temp = pd.DataFrame()
        df_temp[date] = df_oneDay['type']
        counts = pd.concat([counts, df_temp[date].value_counts()], axis=1)

    counts = counts.T
    counts = counts.fillna(0)
    counts.index = pd.to_datetime(counts.index)
    counts['weekday'] = [x.weekday() for x in counts.index]

    return counts

def analyzeCountsLocationOnDate(df, date, setOfType, locationClassification = {}):
    df_temp = df[['latitude', 'longitude', 'note', 'type']].loc[date]
    df_temp = df_temp.sort_index()
    df_temp['longitude'] = df_temp['longitude'].fillna(method='backfill').fillna(method='ffill')
    df_temp['latitude'] = df_temp['latitude'].fillna(method='backfill').fillna(method='ffill')
    df_temp, locationClassification = LA.classifyLocations(df_temp, locationClassification)
    counts = pd.DataFrame(index=setOfType)
    for i in range(24):
        time = i
        if (time < 10):
            time = f"0{time}"
        try:
            df_temp2 = df_temp[f'{date} {time}']
        except:
            continue
        count = df_temp2['type'].value_counts()
        latitude_median = df_temp2['latitude'].median()
        longitude_median = df_temp2['longitude'].median()
        classification_median = df_temp2['classification'].median()
        count = count.append(pd.Series([latitude_median, longitude_median, classification_median], index=['latitude', 'longitude', 'classification']))
        counts[f'{time}'] = count
        # counts[f'{i}'] = pd.concat([counts, count], axis = 1)
    # counts = counts.fillna(0)
    counts = counts.T

    counts.index = date + ' ' + counts.index
    counts.index = pd.to_datetime(counts.index)

    return counts, locationClassification


def getSetOfItemsOfType(df):
    setOfType = util.getSetOfItem(df['type'].dropna())
    itemsForRemove = ['광고', 'Google 애널리틱스', '뉴스', 'Google Play 스토어',  '동영상 검색']
    for i, item in enumerate(itemsForRemove):
        setOfType.remove(item)

    setOfType.extend(['longitude', 'latitude', 'classification'])

    return setOfType


def randomizeValues(df):
    for i, column in enumerate(df.columns):
        df[column] = df[column] + random.ranf(len(df)) / 2 - 0.25
    return df



path_save = r"/Volumes/T7/auto diary/pythonProject/dataAnalyzed/usage"

dataLoader = DataLoader.DataLoader()
df = dataLoader.loadData()

# fig, ax = plt.subplots()

dates = util.getDates(datetime.datetime(2022, 8, 10), 200)
print('aa')

setOfType = getSetOfItemsOfType(df)
resultOfCountAndLocation = pd.DataFrame()

locationClassification = {}
for i, date in enumerate(dates[100:200]):
    print(date)
    try :
        result, locationClassification = analyzeCountsLocationOnDate(df, date, setOfType, locationClassification)
        resultOfCountAndLocation = pd.concat([resultOfCountAndLocation, result])
    except :
        pass

resultCopy = resultOfCountAndLocation.copy()
resultCopy['time'] = resultCopy.index.hour

for i, column in enumerate(resultCopy.columns):
    resultCopy[column] = resultCopy[column] + random.ranf(len(resultCopy))/2 -0.25


fig, ax = plt.subplots(len(resultCopy.columns)-1, 1, sharex= True)
for i, column in enumerate(resultCopy.columns[:-1]):
    ax[i].scatter(resultCopy['classification'], resultCopy[column], s = 1)
    ax[i].set_ylabel(column)

class0 = resultCopy[resultCopy['classification'] == 0]

for i, column in enumerate(class0.columns):
    class0[column] = class0[column] + random.ranf(len(class0))/2 -0.25

class1 = resultCopy[resultCopy['classification'] == 1]

for i, column in enumerate(class1.columns):
    class1[column] = class1[column] + random.ranf(len(class1)) / 2 - 0.25


# class1_time = randomizeValues(class1_time)
for j in range(24):
    class1_time = class1[class1['time'] == j]
    print(j)
    plt.scatter(class1_time['Android'], class1_time['Chrome'], s = 3, label = j, c = 'blue', alpha = (j+5)/30)
    plt.scatter(class1_time['Android'], class1_time['Chrome'], s = 3, label = j, c = [j/24]* len(class1_time), cmap = plt.cm.autumn)

# plt.scatter(class1['Android'],  class1['Chrome'], s = 10, c = class1['time'], cmap = plt.cm.seismic, alpha = 0.5)
# plt.colorbar()

print(resultCopy)
import calmap

for i, date in enumerate(dates):
    column = 'Android'
    classification = 0
    try :
        df_temp3 = resultCopy[date].copy()
        df_temp3 = df_temp3.fillna(0)
        df_temp3 = df_temp3[df_temp3['classification'] == classification ]
        plt.scatter(df_temp3['time'], [i]* len(df_temp3), alpha = df_temp3[column]/ df_temp3[column].max(), c = 'blue')

    except : pass

    plt.title(f'{column}_{classification}')

#
#
# #plot for location
# fig, ax = plt.subplots(1, 1)
# locationClassifications = {}
# j = 150
# dates2 = dates[j:j+20]
# for i , date in enumerate(dates2):
# # for i, date in enumerate(['2022-08-30', '2022-08-29', '2022-08-28', '2022-08-27', '2022-08-26', '2022-08-25', '2022-08-24']):
#     try :
#         df_oneDay = df[date].sort_index()
#         df2, locationClassifications  = LA.classifyLocations(df_oneDay, locationClassifications, threshold = 100)
#         df2.index = [x.hour + x.minute/60 + x.second/3600 for x in df2.index.time]
#         LA.eventPlotLocation(ax, df2, locationClassifications, offset = i+1)
#     except :
#         pass
#
# print(df_oneDay)
# LA.plotLocation(df2, type = 'scatter')
#
# LA.plotScatter(df2)
#
# print(dates[0])
# # LA.plotLocation(df_oneDay['l'])
