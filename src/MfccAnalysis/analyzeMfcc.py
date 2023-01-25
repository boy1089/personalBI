

import os
import glob
import librosa, librosa.display
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import gc

import pandas as pd

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

path = r'/Volumes/T7/auto diary/data/audio'
files_audio = glob.glob(f'{path}/*.m4a')
files_audio.sort(reverse= False)
print(files_audio)
print(files_audio)

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
from datetime import datetime

for i, file in enumerate(files_audio[2:]):

    try :
        duration = librosa.get_duration(filename=file)
        filename = file.split('/')[-1]
        date = filename[:8]
        time = filename[9:15]
        datetime2 = pd.to_datetime(filename[:15].replace('_', '-'))

        for j in range(int(duration / duration_crop)+1):
            print(f'processing {filename}, {j} / {int(duration / duration_crop)+1} th operation')
            average_profile, std_profile, average, std = analyzeAndPlotMFCC(file, offset=duration_crop*j, duration=120, savefile=f'{path_save}/{filename}_{j*duration_crop/60} min.png')
            averageProfileList.append(average_profile)
            stdProfileList.append(std_profile)
            averageList.append(average)
            stdList.append(std)
            filenameList.append(filename)
            dateList.append(date)
            timeList.append(time)
            datetimeList.append(datetime2 + pd.Timedelta(seconds = j * duration_crop))
            # plt.close()
            gc.collect(0)
            gc.collect(1)
            gc.collect(2)

        df2 = pd.DataFrame(np.asarray([filenameList, datetimeList]))
        df3 = pd.DataFrame(np.asarray(averageProfileList))
        df_average = pd.concat([df2.T, df3], axis=1)

        df_average.to_csv(f'{path_save}/averageProfile.csv')

        df3 = pd.DataFrame(np.asarray(stdProfileList))
        df_std = pd.concat([df2.T, df3], axis=1)
        df_std.to_csv(f'{path_save}/stdProfile.csv')

        df = pd.DataFrame(np.asarray([filenameList,datetimeList, averageList, stdList])).T
        df.columns = ['filename', 'datetime', 'average', 'std']
        df.to_csv(f'{path_save}/average, std.csv')

        print('aa')

    except :
        print(f'{i} th file is passed')
        pass
