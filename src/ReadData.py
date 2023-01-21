
import pandas as pd
import zipfile
import os, glob
import matplotlib.pyplot as plt
import pickle
import numpy as np
import datetime as datetime



def defineSensorList():
    sensorList =  [  # 'Accelerometer',
        # 'Annotation',
        'Gravity',
        # 'Gyroscope',
        'Light',
        'Location',
        # 'Metadata',
        # 'Microphone',
        # 'Orientation',
    ]
    return sensorList


def defineStatusList():
    statusList = ['phone motion',
                  'outdoor',
                  'address'
                  ]
    return statusList


def readData(file):
    zf = zipfile.ZipFile(file)
    dataDic = {}

    for i, sensor in enumerate(defineSensorList()):
        try:
            df = pd.read_csv(zf.open(sensor + '.csv'))
            dataDic[sensor] = df
        except:
            print('%s th file passed in readData' % i)
            pass

    return dataDic


def readStatus(file):
    zf = zipfile.ZipFile(file)
    dataDic = {}
    for i, sensor in enumerate(defineStatusList()):
        try:
            df = pd.read_csv(zf.open(sensor + '.csv'))
            dataDic[sensor] = df
        except:
            print('%s th file passed in readData' % i)
            pass

    return dataDic


def saveData(df_dic, file, folder='status', ):
    file = '.\..\data\%s\%s.csv.zip' % (folder, file)
    zf = zipfile.ZipFile(file, 'w')
    for key in df_dic.keys():
        zf.write('%s.csv' % key, df_dic[key].to_csv('%s.csv' % key))
    zf.close()

    return 0


def mergeData(folder, date=''):
    files = glob.glob(folder + r'/*%s*.zip' % date)

    dfDic = {}
    for k, sensor in enumerate(defineSensorList()):
        dfDic[sensor] = pd.DataFrame()
    for i, file in enumerate(files):
        dataDic = readData(file)
        print('reading %s' % file)
        for j, sensor in enumerate(defineSensorList()):
            try:
                print('i, j : ', file, sensor)
                dfDic[sensor] = dfDic[sensor].append(dataDic[sensor])
            except:
                pass

    for i, sensor in enumerate(defineSensorList()):
        dfDic[sensor] = dfDic[sensor].sort_values(by='time')
    return dfDic


def filterData(df):
    filterList = {'Location': ['bearingAccuracy', 'speedAccuracy', 'verticalAccuracy',
                               'horizontalAccuracy', 'speed', 'bearing']}
    for item in filterList:
        df[item].drop(filterList[item], axis=1, inplace=True)

    for i, sensor in enumerate(defineSensorList()):
        if sensor == 'Location':
            df[sensor] = subsample(df[sensor], 50)
            continue

    return df


def plotData(dataDic):
    plt.figure()
    n = len(dataDic)
    plt.subplot('%s1%s' % (n, n))
    for i, sensor in enumerate(defineSensorList()):
        plt.subplot('%s1%s' % (n, str(i + 1)))
        for j, column in enumerate(dataDic[sensor]):
            print(sensor, column)
            if j > 1:
                plt.scatter(pd.to_datetime(dataDic[sensor]['time']), dataDic[sensor][dataDic[sensor].columns[j]], s=1)
            else:
                pass

        plt.ylabel(sensor)
    print('end')


def readMergedData(note):
    if note == '':
        with open('data_merged.pickle', 'rb') as fr:
            user_loaded = pickle.load(fr)

        return user_loaded
    else:

        with open('data_merged.pickle', 'rb') as fr:
            user_loaded = pickle.load(fr)
        return user_loaded


def saveMergedData(data, note):
    if note == '':

        with open('data_merged.pickle', 'wb') as fw:
            pickle.dump(data, fw)

    else:

        with open('data_merge.pickle', 'wb') as fw:
            pickle.dump(data, fw)


def subsample(data, subsampleRate):
    subsampledData = data[::subsampleRate]
    return subsampledData


def printData(df, key):
    print(df[key])


def plotSensor(ax, df, key, num=-1):
    df[key]['time'] = pd.to_datetime(df[key]['time'])
    ax.scatter(df[key]['time'], df[key][df[key].columns[num]], label=df[key].columns[num])
    plt.legend()

    return ax


def plotAll(df):
    numberOfSensor = len(defineSensorList())

    fig, ax = plt.subplots(numberOfSensor, 1, sharex=True)

    for i, sensor in enumerate(defineSensorList()):

        df[sensor]['time'] = pd.to_datetime(df[sensor]['time'])
        for column in df[sensor].columns[2:]:
            ax[i].plot(df[sensor]['time'], df[sensor][column], label=column)

        ax[i].legend()


def changeTimezone(df):
    for i, sensor in enumerate(defineSensorList()):
        df[sensor]['time'] = pd.to_datetime(df[sensor]['time'])
        df[sensor]['time'] = df[sensor]['time'] + pd.Timedelta(hours=9)

    return df


from geopy.geocoders import Nominatim


def convertLocationToAddress(latitude, longitude):
    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse("%s, %s" % (latitude, longitude))
    address = locname.address.split(',')[0]
    print(address)
    return address


def convertLocationInDataframe(df):
    # print(df)
    # print(df['latitude'].iloc[0])
    df['address'] = [0] * len(df)
    for i in range(len(df)):
        df['address'].iloc[i] = convertLocationToAddress(df['latitude'].iloc[i], df['longitude'].iloc[i])

    # print(df.columns)
    return df


if __name__ == '__main__':
    folder = r"../data/prev"
    folder_save = folder + r'/filtered'

    files = glob.glob((folder))

    date = ''

    df = mergeData(folder, date)

    df_temp = pd.DataFrame()
    df_temp['time'] = pd.to_datetime(df['Location']['time'])
    df_temp['time'] = df_temp['time'].dt.round("30s")

    df_temp['longitude'] = df['Location']['longitude']
    df_temp['latitude'] = df['Location']['latitude']

    df_temp2 = pd.DataFrame()

    df_temp2['time'] = pd.to_datetime(df['Gravity']['time'])
    df_temp2['time'] = df_temp2['time'].dt.round("30s")

    df_temp2['accelX'] = df['Gravity']['x']
    df_temp2['accelY'] = df['Gravity']['y']
    df_temp2['accelZ'] = df['Gravity']['z']

    df_temp = df_temp.set_index('time')
    df_temp2 = df_temp2.set_index('time')

    df_temp3 = pd.merge(df_temp, df_temp2, left_index=True, right_index=True)

    plt.plot(df_temp3['longitude'])
    plt.plot(df_temp3['latitude'])
    import datetime

    dates = df_temp3.index.drop_duplicates(keep='first')
    dates_sorted = list(set([x.strftime('%Y%m%d') for x in dates]))
