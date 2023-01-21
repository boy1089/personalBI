import librosa, librosa.display
import matplotlib.pyplot as plt

import glob
from moviepy.editor import *
import util
import pandas as pd
import numpy as np

import playsound
import pyaudio
import wave
import multiprocessing

from datetime import timedelta
import datetime
import gc
class AudioReader:
    def readAudio(self, date, start_index = 0, end_index = -1):

        folders = glob.glob(util.path_log + r'audio')
        files = sorted(glob.glob(folders[0] + fr'/{date}*.m4a'))
        df = pd.DataFrame()
        subsamplingFactor = 44100/4410
        for i, file in enumerate(files[start_index: end_index]):
            print(f'processing {i} / {len(files)} th file ...{file}')
            date, time, _ = file.split('/')[-1].split('_')
            audioClip = AudioFileClip(file, fps = subsamplingFactor)

            soundArray = audioClip.to_soundarray(fps = subsamplingFactor).T[0]#[::subsamplingFactor]
            df_temp = pd.DataFrame()
            df_temp['sound'] = soundArray
            df_temp['time']  = np.arange(0, len(soundArray))#* subsamplingFactor
            timestamp = datetime.datetime.strptime(f'{date} {time}', '%Y%m%d %H%M%S')
            df_temp['time'] = pd.to_datetime(df_temp['time'] / subsamplingFactor, unit = 's', origin = timestamp)
            df = pd.concat([df, df_temp])
            del audioClip
            del soundArray
            del df_temp
            gc.collect()

        df = self.setTimeAsIndexAndSort(df)
        return df

    def readPhoneCall(self, index):

        folders = glob.glob(util.path_log + r'phoneCall')
        files = sorted(glob.glob(folders[0] + fr'/*.m4a'))
        print(files)
        file = files[index]
        print(file)
        date = file.split('/')[-1].split('_')[-1][:8]
        time = file.split('/')[-1].split('_')[-1][8:-4]
        audioClip = AudioFileClip(file)
        return audioClip, date, time

    def convertAudioToArray(self, audioClip, date, time):
        df = pd.DataFrame()
        subsamplingFactor = 44100 / 2
        soundArray = audioClip.to_soundarray(fps=subsamplingFactor).T[0]  # [::subsamplingFactor]
        df_temp = pd.DataFrame()
        df_temp['sound'] = soundArray
        df_temp['time'] = np.arange(0, len(soundArray)) / subsamplingFactor
        timestamp = datetime.datetime.strptime(f'{date} {time}', '%Y%m%d %H%M%S')
        df_temp['time'] = pd.to_datetime(df_temp['time'], unit='s', origin=timestamp)
        df = pd.concat([df, df_temp])
        df = self.setTimeAsIndexAndSort(df)
        return df

    def setTimeAsIndexAndSort(self, df):
        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time')
        df = df.sort_index()
        return df

    #
    # file = r"/Users/jiyoung/PycharmProjects/pythonProject/data/audio/20220816_231219_audio.m4a"
    # audioclip = AudioFileClip(file)
    # # audioclip.write_audiofile(file.replace('.mp4', '.wav'))
    # # subclip = audioclip.subclip(f'00:30:00', f'00:31:00')
    # print("file loaded")
    # print(audioclip.to_soundarray())
    # import matplotlib.pyplot as plt
    # a = audioclip.to_soundarray()R
    # b = a.T[0]
    # plt.plot(b)
    def getDateRange(self, startDate = None, endDate = None):
        if startDate == None:
            startDate = self.data.index[0].date()
            endDate = self.data.index[-1].date()

        numberOfDate = (endDate - startDate).days
        self.dateList = [endDate - datetime.timedelta(days=x) for x in range(numberOfDate)]
        return self.dateList

if __name__ == "__main__":



    # a = AudioReader()
    # b = a.readAudio("20220910", 0, 1)
    path = r"/Volumes/T7/auto diary/pythonProject/data/audioArray/20220825_audioArray.csv"
    path = r"/Volumes/T7/auto diary/pythonProject/data/audioArray/20220828_audioArray.csv"
    df = pd.read_csv(path)
    print(df.columns)
    plt.plot(df['sound'])
    c = librosa.stft(df['sound'].values, n_fft = 500)
    d = np.abs(np.log(c))
    plt.imshow(d, aspect = 30)

    print('a')




    ''' for converting audio files'''
    '''
    path = r"/Volumes/T7/auto diary/pythonProject/data/phoneCall/0313250471_20220805162536.m4a"

    a = AudioReader()
    dateRange = a.getDateRange(datetime.datetime.strptime("20220901", '%Y%m%d'), datetime.datetime.strptime("20220917", '%Y%m%d'))
    for i, date in enumerate(dateRange):
        try :
            date = datetime.datetime.strftime(date, '%Y%m%d')
            b = a.readAudio(date)
            print('a')
            b.to_csv(f'../data/' + fr'audioArray_small/{date}_audioArray_small.csv')
        except :
            print(f'failed in {date}')

    print('b')
    '''
