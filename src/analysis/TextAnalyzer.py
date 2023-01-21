
import sys
from wordcloud import WordCloud
from konlpy.tag import Twitter
from collections import Counter
import glob
import json
import pandas as pd
import datetime as datetime


from matplotlib import rc, font_manager
import matplotlib.pyplot as plt
import matplotlib
rc('font',family='AppleGothic')
matplotlib.use('TkAgg')

font_fname = '/Volumes/T7/auto diary/pythonProject/src/NanumSquareNeo-aLt.ttf'
font_family = font_manager.FontProperties(fname=font_fname).get_name()
path = r"/Volumes/T7/auto diary/pythonProject/dataAnalyzed/audio_term 5sec"


def parseDatetimeFromFilename(filename):
    filename_splitted = filename.split('/')[-1]
    date = filename_splitted[:8]
    time = filename_splitted[9:15]
    return date, time


def createWordCloud(listOfWords):
    counts_oneFile = Counter(listOfWords)
    tags = counts_oneFile.most_common(100)

    wc = WordCloud(font_path=font_fname, background_color="white", max_font_size=60, width=1000)

    cloud = wc.generate_from_frequencies(dict(tags))

    return cloud, tags


files = glob.glob(f'{path}/*.json')
df = pd.DataFrame()
for i, file in enumerate(files):
    try :

        with open(files[i], 'r', encoding = 'utf-8-sig') as file:
            json_data = json.load(file)

        json_data['data'] = json_data['data']
        date, time = parseDatetimeFromFilename(files[i])

        df = pd.concat([df, pd.DataFrame([datetime.datetime.strptime(f"{date}_{time}", "%Y%m%d_%H%M%S"), json_data['data']])], axis = 1)
    except :
        pass
    # df = df.append([datetime.datetime.strptime(f"{date}_{time}", "%Y%m%d_%H%M%S"), json_data['data']])

df = df.T
df.columns = ['datetime', 'data']
df2 = df[df.data.notnull()]
df2['date'] = pd.to_datetime(df2['datetime']).dt.date

df2 = df2.sort_values(by="datetime")
print(df2['data'])

setOfDate = list(set(df2['date'].tolist()))
setOfDate.sort()

listOfCloud = []
for i, date in enumerate(setOfDate):
    df_temp = df2[df2['date'] == date]
    wordList = []
    for j in range(len(df2)):
        try :
            wordList.extend(df_temp.iloc[j].data.split(' '))
        except :
            pass
    wordList = [x for x in wordList if len(x) > 1]
    if(len(wordList)==0): continue
    cloud, tags = createWordCloud(wordList)

    listOfCloud.append([cloud, wordList])

print(listOfCloud[0][0])

for i, entry in enumerate(listOfCloud):
    print(entry)

fig, ax = plt.subplots(10, 4, figsize = (30, 20))
a = 0
for i, cloud in enumerate(listOfCloud[:40]):
    ax[i % 10][int(i / 10)].imshow(cloud[0])
    ax[i % 10][int(i / 10)].set_title(setOfDate[i].strftime("%Y-%m-%d"))
    ax[i % 10][int(i / 10)].set_ylabel(len(cloud[1]))
    a+=len(cloud[1])
    print(a)

fig.savefig("/Volumes/T7/auto diary/pythonProject/dataAnalyzed/audio_term 5sec_word cloud/test.png")

