import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import datetime

import DataLoader
import util


#TODO : analyze google data
#TODO : give summary of week, month day
#TODO :

class DataAnalyzer:

    def __init__(self, data):
        self.data = data
        self.getDateRange()

    def getSummaryOfDates(self, startDate, endDate):
        print(f"dataAnalyzer, getSummary of Dates {startDate} ~ {endDate}")
        dates = self.getDateRange(datetime.datetime.strptime(startDate, '%Y%m%d'), datetime.datetime.strptime(endDate, '%Y%m%d'))

        df = pd.DataFrame()
        for i, date in enumerate(dates):
            print(f"analyzing {date}...")
            df_date = self.getSummaryOfDate(date)
            df_date.index = [date]
            df = pd.concat([df, df_date], axis = 0)

        return df


    def getSummaryOfDate(self, date):

        dataOriginal = self.getDataOfDate(date)
        dataLocation = self.analyzeDailyActivity(dataOriginal)

        columns = ['location_std', 'timeSpentOnEachLocation',
                   'deposit_count', 'withdraw_count', 'accel_std', 'image_count','phoneCall_count']

        timeSpentOnEachLocation = self.getTimeDurationForEachState(dataLocation);

        #TODO : add expense,
        #TODO : make summary with UI.

        # self.analyzeGoogleActivity(data, DataReader.googleDataTypeList[1])

        location_std = dataOriginal['longitude'].std() + dataOriginal['latitude'].std()
        # location_home = True if data['location'].eq("home").any(0) ==True else False
        # location_work= True if data['location'].eq("work").any(0) == True else False

        deposit_count = dataOriginal['입금액'].count()
        withdraw_count = dataOriginal['출금액'].count()
        dataOriginal['accelZ'] = dataOriginal['accelZ'].astype(float)

        accel_std = dataOriginal['accelX'].std() + dataOriginal['accelY'].std() + dataOriginal['accelZ'].std()



        image_count = dataOriginal['file'].count()
        phoneCall_count = dataOriginal['name'].count()

        df = pd.DataFrame([[location_std,  timeSpentOnEachLocation,
                            deposit_count, withdraw_count, accel_std, image_count, phoneCall_count,
                            ]],
                          columns = columns, index = [date])

        return df

    def analyzeGoogleActivity(self, df, type):
        df_temp = df[df['type'] == type]

        numberOfActivity = df_temp.count()
        pass

    def analyzeWhetherWorked(self, df):
        df_original = df
        df['distance_home'] = np.sqrt((df['latitude'] - self.latitude_home)**2 + (df['longitude'] - self.longitude_home)**2)
        df['distance_work'] = np.sqrt((df['latitude'] - self.latitude_work)**2 + (df['longitude'] - self.longitude_work)**2)

        df['location'] = None
        locationList = []
        for j in range(len(df)):
            if df['distance_home'].iloc[j] < 0.002:
                locationList.append('home')
            elif df['distance_work'].iloc[j] < 0.02:
                locationList.append('work')
            else :
                locationList.append('None')
        df_original['location'] = locationList
        return df_original
    def analyzeWorkingTime(self, df):
        df_atwork = df['location'][df['location'] == 'work'].sort_index()
        datetimeArrivedWork = df_atwork.index[0]
        datetimeLeavingWork = df_atwork.index[-1]
        timeSpendInWork = datetimeLeavingWork - datetimeArrivedWork

        return datetimeArrivedWork, datetimeLeavingWork, timeSpendInWork

    def getDataOfDate(self, date):
        if type(date) != str:
            date = date.strftime('%Y%m%d')
        data1 = self.data.loc[date].sort_index()
        data1.index = [datetime.datetime.combine(datetime.date(1970, 1, 1), x.time()) for x in data1.index]
        return data1


    def datetimeToString(date):
        return date.strftime('%Y%m%d')

    def getWeek2(self, year, week, column):

        data_week = pd.DataFrame()
        for day in range(1, 8):
            date = datetime.date.fromisocalendar(year, week, day)
            data_temp = self.getDate(date, 'latitude')
            data_temp = data_temp.resample(rule = '60S').first()
            data_temp.name = date.strftime('%Y%m%d')
            # data_temp = data_temp.rename(columns = {'latitude': date.strftime('%Y%m%d')})

            data_week = pd.concat([data_week, data_temp], axis = 1)
        return data_week

    def getDateRange(self, startDate = None, endDate = None):
        if startDate == None:
            startDate = self.data.index[0].date()
            endDate = self.data.index[-1].date()

        numberOfDate = (endDate - startDate).days
        self.dateList = [endDate - datetime.timedelta(days=x) for x in range(numberOfDate)]
        return self.dateList


    def analyzeDailyActivity(self, data):

        #get data of specific date
        # df= self.getDataOfDate(date)

        #get the columns related to location and remove na
        df = self.selectLocationColumns(data)
        df = self.calculateDistanceFromWork(df)
        df = self.calculateDistanceFromHome(df)
        df = self.getLocationState(df)

        if (len(df.index)==0) :
            return df

        # overwrite the status if location is changing.
        # df = self.getMovingState(df)

        return df
    def getTimeDurationForEachState(self, df):

        timeSpent = {util.locationState_home : np.timedelta64(0),
                     util.locationState_work : np.timedelta64(0),
                     util.locationState_moving : np.timedelta64(0),
                     util.locationState_NA : np.timedelta64(0) }

        if (len(df.index) == 0 ):
            return timeSpent

        previousState = 0
        startOfState = df.index.values[0]
        for j in range(len(df)):
            currentState = df['locationState'][j]
            if (currentState != previousState) :
                timeSpentOnState = df.index.values[j] - startOfState
                # print(f"{currentState}, {previousState}, {timeSpentOnState.astype('timedelta64[s]').astype(np.int32)/3600.0}")
                timeSpent[previousState] += timeSpentOnState
                previousState = currentState
                startOfState = df.index.values[j]


        for key in timeSpent.keys():
            timeSpent[key] = timeSpent[key].astype('timedelta64[s]').astype(np.int32) #unit conversion from ns to second ( int)
            timeSpent[key] = timeSpent[key] /3600.0

        return timeSpent
    def selectLocationColumns(self, df):
        df = df[['latitude', 'longitude']].dropna()
        return df
    def calculateDistanceFromHome(self, df):
        df['distance_home'] = np.sqrt(
            (df['latitude'] - util.latitude_home) ** 2 + (df['longitude'] - util.longitude_home) ** 2)
        return df

    def calculateDistanceFromWork(self, df):
        df['distance_work'] = np.sqrt(
            (df['latitude'] - util.latitude_work) ** 2 + (df['longitude'] - util.longitude_work) ** 2)
        return df

    def getLocationState(self, df):
        df['locationState'] = None
        locationList = []
        for j in range(len(df)):
            if df['distance_home'].iloc[j] < util.location_home_threshold:
                locationList.append(util.locationState_home)
            elif df['distance_work'].iloc[j] < util.location_work_threshold:
                locationList.append(util.locationState_work)
            else :
                locationList.append(util.locationState_NA)
        df['locationState'] = locationList

        return df

    def getMovingState(self, df):
        latitudeChangeRate = np.convolve(df['latitude'].diff(50).abs(), [1/50]*50)
        longitudeChangeRate = np.convolve(df['longitude'].diff(50).abs(), [1/50] *50)
        for j in range(len(df)-50):
            if (latitudeChangeRate[j] + longitudeChangeRate[j] > util.locationState_moving_threshold) :
                df['locationState'][j] = util.locationState_moving

        return df



    def convertTimeToTheta(self, df):
        df['theta'] = df.index.values.astype(int) /1e9 / 3600 / 24 * 2 * np.pi

        return df


if __name__ == "__main__":


    dataLoader = DataLoader.DataLoader()
    data = dataLoader.loadData()

    dataAnalyzer = DataAnalyzer(data)
    data_summary = dataAnalyzer.getSummaryOfDates('20220717', '20220830')
    # data_summary = dataAnalyzer.getSummaryOfDate('20220731')

    df_temp = data.loc['20220811']
    # df_temp = data
    df_temp2 = dataAnalyzer.analyzeDailyActivity(df_temp)
    a = dataAnalyzer.getTimeDurationForEachState(df_temp2)

    fig, ax = plt.subplots()

    fig, ax = plt.subplots(subplot_kw = {'projection': 'polar'})
    ax.plot((df_temp2['longitude'] - df_temp2['longitude'].min())*10, label = 'longitude_scaled')
    ax.plot(df_temp2['locationState'], label = 'locationState')
    ax.legend()


    ax.plot(data.loc['20220515']['latitude'])

    print(data_summary.loc['2022-08-09']['timeSpentOnEachLocation'])

    fig, ax = plt.subplots()
    ax.plot(data_summary.index, [x[1.2] for x in data_summary['timeSpentOnEachLocation']])
    print(data_summary)

    print('a')
    print('a')


