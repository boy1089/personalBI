

import os
import glob
import librosa, librosa.display
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import gc

import pandas as pd

import src.util as util
def delete_me(obj):
    referrers = gc.get_referrers(obj)
    for referrer in referrers:
        if type(referrer) == dict:
            for key, value in referrer.items():
                if value is obj:
                    referrer[key] = None

def analyzeAndPlotMFCC(file, offset = 0, duration = 120, savefile = None):
    # file = files_audio[7]
    sig, sr = librosa.load(file, sr=44100, offset=offset, duration= duration)
    sig2, _ = librosa.effects.trim(sig)

    n_fft = 2048
    hop_length = 512
    n_mels = 128
    #
    S = librosa.feature.melspectrogram(y =sig2, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
    b = librosa.feature.mfcc(y = sig, sr=sr)

    fig, ax = plt.subplots(nrows=3, sharex=False, figsize = (20, 15))
    c = librosa.power_to_db(S = S, ref=np.max)
    img = librosa.display.specshow(c,
                                   x_axis='time', y_axis='mel', fmax=8000,
                                   ax=ax[0])
    d = fig.colorbar(img, ax=[ax[0]])
    ax[0].set(title='Mel spectrogram')
    ax[0].label_outer()
    img = librosa.display.specshow(b, x_axis='time', ax=ax[1])
    e = fig.colorbar(img, ax=[ax[1]])
    ax[1].set(title='MFCC')

    characteristicOfContext_average_profile = np.average(b, axis=1)
    characteristicOfContext_std_profile = np.std(b, axis=1)
    characteristicOfContext_average = np.average(b)
    characteristicOfContext_std = np.std(b)

    ax[2].plot(characteristicOfContext_average_profile, label=characteristicOfContext_average)
    ax[2].plot(characteristicOfContext_std_profile, label=characteristicOfContext_std)
    ax[2].set_ylim(-700, 200)

    plt.legend(loc='upper right')

    if savefile!=None:
        plt.savefig(savefile)
    plt.close(fig)
    plt.close(1)
    obj_list = [fig, ax, sig, S, b, sr, c, d, e, img, sig2]
    for obj in obj_list:
        delete_me(obj)
        del(obj)

    gc.collect()
    return list(characteristicOfContext_average_profile), list(characteristicOfContext_std_profile), characteristicOfContext_average, characteristicOfContext_std







path_audio = r'/Volumes/T7/auto diary/data/audio'
path_summary = r'/Volumes/T7/auto diary/dataAnalyzed/mfcc analysis/average, std.csv'
path_average_profile = r'/Volumes/T7/auto diary/dataAnalyzed/mfcc analysis/averageProfile.csv'
path_std_profile = r'/Volumes/T7/auto diary/dataAnalyzed/mfcc analysis/stdProfile.csv'

df_summary = pd.read_csv(path_summary)
df_average_profile = pd.read_csv(path_average_profile)
df_std_profile = pd.read_csv(path_std_profile)
df_average_profile = df_average_profile[df_average_profile.columns[1:]]
df_std_profile = df_std_profile[df_std_profile.columns[1:]]


setOfFilename = util.getSetOfItem(df_summary['filename'])
df_average_profile.columns = range(df_average_profile.columns.size)
df_std_profile.columns = range(df_std_profile.columns.size)

files_audio = glob.glob(f'{path_audio}/*.m4a')
files_audio.sort(reverse= False)

path_save = r'/Volumes/T7/auto diary/dataAnalyzed/mfcc analysis'
duration_crop = 120

averageProfileList = []
stdProfileList = []
averageList =[]
stdList = []
filenameList = []
dateList = []
timeList = []
datetimeList = []
statusList = []

import time as time2
for i, file in enumerate(files_audio[2:]):
    filename = file.split('/')[-1]
    if(filename in setOfFilename):
        print(f'{filename} is already processed!')
        continue

    try :
        duration = librosa.get_duration(filename=file)
        date = filename[:8]
        time = filename[9:15]
        datetime2 = pd.to_datetime(filename[:15].replace('_', '-'))

        for j in range(int(duration / duration_crop)+1):
            start = time2.time()
            average_profile, std_profile, average, std = analyzeAndPlotMFCC(file, offset=duration_crop*j, duration=120, savefile=f'{path_save}/{filename}_{j*duration_crop/60} min.png')

            time1 = time2.time()
            status = j == int(duration / duration_crop)
            averageProfileList.append(average_profile)
            stdProfileList.append(std_profile)
            averageList.append(average)
            stdList.append(std)
            filenameList.append(filename)
            dateList.append(date)
            timeList.append(time)
            datetimeList.append(datetime2 + pd.Timedelta(seconds = j * duration_crop))
            statusList.append(status)
            end = time2.time()
            print(f'processing {filename}, {j} / {int(duration / duration_crop)+1} th operation done, time elapsed : {end - start}, time1 : {time1 - start}')

            # plt.close()


        df_prefix = pd.DataFrame(np.asarray([filenameList, datetimeList]))

        df3 = pd.DataFrame(np.asarray(averageProfileList))
        df_average = pd.concat([df_prefix.T, df3], axis=1)
        df_average.columns = range(df_average.columns.size)

        df_average_profile = pd.concat([df_average_profile, df_average], axis = 0)
        df_average_profile.to_csv(f'{path_save}/averageProfile.csv')

        df3 = pd.DataFrame(np.asarray(stdProfileList))
        df_std = pd.concat([df_prefix.T, df3], axis=1)
        df_std.columns = range(df_std.columns.size)

        df_std_profile = pd.concat([df_std_profile, df_std], axis = 0)
        df_std_profile.to_csv(f'{path_save}/stdProfile.csv')

        df_summary_temp = pd.DataFrame(np.asarray([filenameList,datetimeList, averageList, stdList, statusList])).T
        df_summary_temp.columns = ['filename', 'datetime', 'average', 'std', 'status']
        df_summary = pd.concat([df_summary, df_summary_temp], axis = 0)

        df_summary.to_csv(f'{path_save}/average, std.csv')

        gc.collect(0)
        gc.collect(1)
        gc.collect(2)

    except :
        print(f'{i} th file is passed')
        pass


    print('aa')