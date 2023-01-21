import itertools

import pandas as pd
import matplotlib.pyplot as plt
import util
import glob
import matplotlib
import zipfile
import numpy as np
# from bs4 import BeautifulSoup

# from moviepy.editor import AudioFileClip
import datetime

import unicodedata
import DataSaver

import calmap
import sys
from wordcloud import WordCloud
from konlpy.tag import Twitter
from collections import Counter


from matplotlib import rc, font_manager

import DataLoader
rc('font',family='AppleGothic')
matplotlib.use('TkAgg')
desired_width=320
pd.set_option('display.width', desired_width)
# np.set_printoption(linewidth=desired_width)
pd.set_option('display.max_columns',10)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 1000)

np.set_printoptions(threshold=sys.maxsize)

sensorList = [
    'Location',
    'Gravity',
    # 'Light',
]

googleDataTypeList = [
    '개발자', '검색', '광고', '뉴스', '동영상 검색', '이미지 검색', 'Android',
    'Chrome', 'Google 애널리틱스', 'YouTube','Google Play 스토어']


class DataReader:


    def readData(self, dataType):
        folders=  glob.glob(util.path_log)

        if dataType == util.dataType_image:
            folder = [x for x in folders if x.find('imagesAll') != -1][0]
            files = glob.glob(folder + r'/*.jpg')
            print(f'processing {len(files)} images..')
            files = [x for x in files if len(x) == 37]

            df = pd.DataFrame()
            dateList = []
            timeList = []
            datetimeList = []
            for i, file in enumerate(files):
                print(i, len(files), file)
                filename = file.split('/')[-1]
                try :
                    date = filename.split('_')[0]
                    time = filename.split('_')[1][:6]
                except :
                    date = filename.split('-')[0]
                    time = filename.split('-')[1][:6]

                try :

                    datetime2 = datetime.datetime.strptime(f'{date} {time}', '%Y%m%d %H%M%S')
                    dateList.append(date)
                    timeList.append(time)
                    datetimeList.append(datetime2)
                except :
                    continue
            df = pd.DataFrame([datetimeList, files]).T
            df.columns = ['time', 'file']
            df = df.set_index('time')
            print(df)




        if dataType == util.dataType_sensor:
            folder = [x for x in folders if x.find('sensor') != -1][0]
            files = glob.glob(folder + r'/*.csv')
            print(files)
            df = pd.DataFrame()
            for i, file in enumerate(files):
                print(file)
                df_temp = pd.read_csv(file)
                df = pd.concat([df, df_temp])
            df.columns = [x.strip() for x in df.columns]


        if dataType == util.dataType_account:
            folder = [x for x in folders if x.find('account')!= -1][0]
            files = glob.glob(folder + r'/*.csv')
            df = pd.DataFrame()
            for i, file in enumerate(files):
                df_temp = pd.read_csv(file)
                df = pd.concat([df, df_temp])

        if dataType == util.dataType_prev:
            folder = [x for x in folders if x.find('prev') != -1][0]
            files = glob.glob(folder + r'/*.zip')

            df = pd.DataFrame()
            for j, file in enumerate(files):
                print(f"processing {file}...")
                zf = zipfile.ZipFile(file)
                df_temp = pd.DataFrame()

                for i, sensor in enumerate(sensorList):
                    try:
                        df_temp2 = pd.read_csv(zf.open(sensor + '.csv'))
                        df_temp2['time'] = pd.to_datetime(df_temp2['time']) + pd.Timedelta(hours = 9)
                        df_temp2 = df_temp2.set_index('time')

                        df_temp = pd.concat([df_temp, df_temp2], axis = 1, join = 'outer')

                    except:
                        print('%s th file passed in readData' % i)
                        pass

                df = pd.concat([df, df_temp])
            df = df.rename(columns = {'x':'accelX', 'y':'accelY', 'z':'accelZ'})
            df = df[['latitude', 'longitude', 'accelX', 'accelY', 'accelZ']]


        if dataType ==  util.dataType_account:
            folder = [x for x in folders if x.find('account') != -1][0]

            files_nh = glob.glob(folder + r'/nh*/*.xls')
            files_kb = glob.glob(folder + r'/kb*/*.xls')
            print(files_kb)

            df = pd.DataFrame()
            for j, file in enumerate(files_nh):
                df_temp = pd.read_excel(file, engine = 'xlrd', skiprows = 7, skipfooter = 1)
                df_temp = df_temp.replace('(.*)\n(.*)', r'\1 \2', regex= True)
                df_temp = df_temp[['거래일시', '출금금액', '입금금액', '거래후잔액', '거래기록사항']]
                df_temp['은행'] = 'nh'
                df = pd.concat([df, df_temp])

            df = df.rename(columns = {'거래일시':'time', '거래후잔액': '잔액', '거래기록사항':'note',
                                      '출금금액': '출금액', '입금금액': '입금액'})


            for j, file2 in enumerate(files_kb):
                print(file2)
                # df_temp = pd.read_excel(file2, engine = 'xlrd', skiprows = 3)
                df_temp = pd.read_html(file2)[2]
                df_temp.columns = df_temp.loc[0]
                df_temp = df_temp[1:-1]

                print(df_temp.columns)

                df_temp = df_temp[['거래일시', '출금액', '입금액', '잔액', '보낸분/받는분']]
                df_temp = df_temp.rename(columns = {'보낸분/받는분' :'note', '거래일시':'time'})
                df_temp['은행'] = 'kb'
                df_temp['입금액'] = df_temp['입금액'].astype('int')
                df_temp['출금액'] = df_temp['출금액'].astype('int')
                df_temp['잔액'] = df_temp['잔액'].astype('int')

                df = pd.concat([df, df_temp])



            df = self.setTimeAsIndexAndSort(df)

            print(df)
        if dataType == util.dataType_google:
            df = pd.DataFrame()
            for i, googleDataType in enumerate(googleDataTypeList):
                print(f'processing {googleDataType}...')
                df_temp = self.readGoogleData(folders, googleDataType)
                df = pd.concat([df, df_temp])
            # df['datetime'] = pd.to_datetime(df['datetime'])
            # df = df.set_index('datetime')


        if dataType == util.dataType_phoneCall:
            print(folders)
            folder = [x for x in folders if x.find('phoneCall') != -1][0]

            files = glob.glob(folder + r'/*.m4a')
            df = pd.DataFrame()

            nameList = []
            phoneNumberList = []
            datetimeList = []

            for i, file in enumerate(files):
                if len(file.split('_')) == 2:
                    name = None
                    phoneNumber = file.split('_')[0]
                    datetime_str = file.split('_')[1][:-3]

                if len(file.split('_')) == 3:
                    name = file.split('_')[0].split('/')[-1]
                    phoneNumber = file.split('_')[1]
                    datetime_str = file.split('_')[2][:-3]
                else :
                    continue

                nameList.append(unicodedata.normalize('NFC', name))
                phoneNumberList.append(phoneNumber)
                datetimeList.append(datetime_str)
            df = pd.DataFrame(np.asarray([nameList, phoneNumberList, datetimeList]).T, columns = ['name', 'phoneNumber', 'datetime'])
            df['datetime'] = pd.to_datetime(df['datetime'])

            df = df.set_index('datetime')

        # if dataType == util.dataType_audio2:
        #     print('bbb')
            # self.readAudioData(folders)



        if df.index.dtype != "datetime64[ns]" :
            df = self.setTimeAsIndexAndSort(df)


        return df.sort_index()

    def readGoogleData(self, folders, type):

        folder = [x for x in folders if x.find('google') != -1][0]
        files = glob.glob(folder + fr'/Takeout*/내 활동/{type}/*')

        activityList = []
        for j, file in enumerate(files):
            with open(files[0], 'rt') as myfile:
                for myline in myfile:

                    texts = myline.split('>')
                    for i , text in enumerate(texts):
                        referenceText = '<a href='


                        if text.find(referenceText) == -1:

                            continue
                        if text.find('다음 설정이') == -1:
                            link = None
                            note = None
                            time = None

                            try :
                                link = text[text.find(referenceText) + len(referenceText)+1:-1]
                                note = texts[i+1][:-3]
                                time = texts[i+3][:-5]
                                activityList.append((link, note, time))
                            except:
                                pass

        #TODO : fix error cases. time = None, "", "KST in link"
        df = pd.DataFrame(np.asarray(activityList), columns = ['link', 'note', 'time'])

        df['time'] = [x.replace('오전', 'AM') for x in df['time']]
        df['time'] = [x.replace('오후', 'PM') for x in df['time']]
        df = df[df['time'].str.find(' KST') != -1]

        df['time'] = pd.to_datetime(df['time'], format = '%Y. %m. %d. %p %I:%M:%S KST')
        df['type'] = [type] * len(df)
        # df = df.set_index('time')
        print(df)

        return df



    def setTimeAsIndexAndSort(self, df):
        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time')
        df = df.sort_index()
        return df

    def mergeData(self):
        imageData = self.readData(util.dataType_image)
        sensorData = self.readData(util.dataType_sensor)
        prevData = self.readData(util.dataType_prev)
        accountData = self.readData(util.dataType_account)
        phoneCallData = self.readData(util.dataType_phoneCall)

        # mergedData = pd.concat([sensorData, prevData, accountData, imageData, phoneCallData])

        googleData = self.readData(util.dataType_google)
        print('aa')
        imageData = imageData.loc[pd.notnull(imageData.index)]


        phoneCallData['time'] = phoneCallData.index
        phoneCallData = phoneCallData.set_index('time')
        print(phoneCallData.index)

        print(sensorData)
        sensorData2 = sensorData[sensorData.index > '2021']
        print(sensorData)
        print(accountData)
        sensorData2 = sensorData2[~sensorData2.index.duplicated(keep = 'first')]

        # mergedData = pd.concat([sensorData2, accountData])
        #
        # mergedData = pd.concat([sensorData, prevData, accountData, imageData, googleData, phoneCallData], join = 'inner')

        mergedData = pd.concat([ prevData, accountData, imageData, googleData, phoneCallData])

        return mergedData


if __name__ =="__main__":
    dataReader = DataReader()

    data = dataReader.mergeData()
    dataSaver = DataSaver.DataSaver()
    dataSaver.saveData(data, 'raw2.csv')


    print('aa')

    googleData = dataReader.readData(util.dataType_google)
    #
    # def getDateRange(startDate = None, endDate = None):
    #     numberOfDate = (endDate - startDate).days
    #     dateList = [endDate - datetime.timedelta(days=x) for x in range(numberOfDate)]
    #     return dateList
    #
    # def getSummaryOfDates(startDate, endDate, df_input):
    #     print(f"dataAnalyzer, getSummary of Dates {startDate} ~ {endDate}")
    #     print(type(startDate))
    #     if(isinstance(startDate, str)):
    #         print('a')
    #         startDate = datetime.datetime.strptime(startDate, '%Y%m%d')
    #         endDate = datetime.datetime.strptime(endDate, '%Y%m%d')
    #     dates = getDateRange(startDate, endDate)
    #     print(dates)
    #
    #     df = pd.DataFrame()
    #     for i, date in enumerate(dates):
    #         numberOfActivity = df_input[datetime.datetime.strftime(date, '%Y%m%d')].count()[0]
    #         df = df.append(pd.DataFrame([date, numberOfActivity]).T)
    #     df.columns = ['date', 'num']
    #     return df
    #
    # a = getSummaryOfDates("20220101", "20220707", googleData['2022'])
    # print(a)
    # plt.plot(a['num'])
    # a = a.set_index('date')
    # a.index = [x.to_pydatetime() for x in a.index]
    # a = a.dropna()
    # # fig, ax2 = plt.figure()
    # a['num'] = a['num'].astype(int)

    # print(googleData['20220101'])
    noteList = googleData['note']

    # print(noteList)

    # ax, plot_data, colormesh = calmap.yearplot(a['num'])

    # twitter = Twitter()

    # twitter함수를 통해 읽어들인 내용의 형태소를 분석한다.
    # sentences_tag = []
    # sentences_tag = twitter.pos(noteList.values)

    noun_adj_list = []

    # tag가 명사이거나 형용사인 단어들만 noun_adj_list에 넣어준다.
    # for word, tag in sentences_tag:
    #     if tag in ['Noun', 'Adjective']:
    #         noun_adj_list.append(word)

    year = '2021'
    month = 7
    month_end = month + 1

    def getCloud(year, month, type):
        print('b')
        month_start = month
        month_end = month+1

        if month < 10:
            month_start = "0"+ str(month)

        if month_end < 10:
            month_end = "0" + str(month_end)

        # noun_adj_list_month = googleData[googleData['type'] == '검색'][f'{year}{month_start}01':f'{year}{month_end}01']['note']
        noun_adj_list_month = googleData[googleData['type'] == type][f'{year}{month_start}02':f'{year}{month_end}03']['note']

        noun_adj_list_year = googleData[googleData['type'] == type][f'{year}':f'{year}']['note']

        noun_adj_list_month = [x.lower() for x in noun_adj_list_month]
        noun_adj_list_year = [x.lower() for x in noun_adj_list_year]

        print('a')
        noun_adj_list2 = []
        for j in range(len(noun_adj_list_month)):
            noun_adj_list2.extend(noun_adj_list_month[j].split(" "))

        noun_adj_list3 = []
        for j in range(len(noun_adj_list_year)):
            noun_adj_list3.extend(noun_adj_list_year[j].split(" "))


        noun_adj_list2 = [x for x in noun_adj_list2 if len(x)>4]
        noun_adj_list3 = [x for x in noun_adj_list3 if len(x)>4]

        # 가장 많이 나온 단어부터 40개를 저장한다.
        counts_month = Counter(noun_adj_list2)
        counts_year = Counter(noun_adj_list3)

        tags_month = counts_month.most_common(100)
        tags_year = counts_year.most_common(100)

        array = np.asarray(tags_year)
        #
        # for i, value in enumerate(tags_month):
        #     if value[0] in array.T:
        #         tags_month.remove(value)

        print(tags_month)
        print(tags_year)

        font_fname = '/Volumes/T7/auto diary/pythonProject/src/NanumSquareNeo-aLt.ttf'
        font_family = font_manager.FontProperties(fname=font_fname).get_name()
        wc_month = WordCloud(font_path=font_fname, background_color="white", max_font_size=60, width = 1000)
        # cloud = wc.generate_from_frequencies(dict(tags[10:]))
        cloud = wc_month.generate_from_frequencies(dict(tags_month))

        return cloud, tags_month
        # plt.imshow(cloud)
    clouds = []
    i = 0
    for i in range(6):
        clouds.append(getCloud(2022, i+1, '광고'))
    print(googleData['type'].value_counts())

    print(googleData[googleData['type'] == '광고'])
    def getDateRange(startDate = None, endDate = None):
        numberOfDate = (endDate - startDate).days
        dateList = [endDate - datetime.timedelta(days=x) for x in range(numberOfDate)]
        return dateList

    # dateList = getDateRange(datetime.datetime.fromisocalendar(year = 2022, month = 8, day = 1), datetime.datetime.fromisocalendar(year = 2022, month = 8, day = 30))
    dateList = getDateRange(datetime.datetime.fromisoformat("2022-03-01 00:00:00"), datetime.datetime.fromisoformat("2022-08-29 00:00:00") )
    for date in dateList :
        print(date.date())
        date = date.date().strftime("%Y%m%d")
        try :
            googleData[date].to_csv(f'/Volumes/T7/auto diary/pythonProject/src/test/{date}.csv')
        except :
            pass
        print(googleData["20220801"].to_csv('/Volumes/T7/auto diary/pythonProject/src/test/test.csv'))

    # data = np.asarray(clouds[0][1])
    # data2 = data.T
    # plt.plot(list(data2[1]), list(data2[0]))
    fig, ax = plt.subplots(6, 2)
    for i, cloud in enumerate(clouds):
        ax[i%6][int(i/6)].imshow(cloud[0])
