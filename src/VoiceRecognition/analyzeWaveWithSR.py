import os
import zipfile

import glob 
import matplotlib.pyplot as plt
import speech_recognition as sr
import glob
import os

from pydub import AudioSegment
from pydub.playback import play
# -*- coding: utf-8 -*-
import sys, re, glob, ffmpeg
import pydub
import numpy as np
import json
TYPE:str = "wav"
FILE_PATH:str  = ".\*.[Mm][Pp]4"
FILE_PATH:str = r"*.mp4"


def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_file(f, "mp4")
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2 ** 15
    else:
        return a.frame_rate, y


r = sr.Recognizer()

path = r"/Volumes/T7/auto diary/pythonProject/data/phoneCall"
path_save = '/Volumes/T7/auto diary/pythonProject/dataAnalyzed/phoneCall_tex`rm 5sec'

path = r"/Volumes/T7/auto diary/pythonProject/data/audio"
path_save = r"/Volumes/T7/auto diary/pythonProject/dataAnalyzed/audio_term 5sec"

length = 1*60*60 + 36*60
term = 5
if (os.path.exists(path_save)== False):
    os.mkdir(path_save)
files = glob.glob(f'{path}/*.wav')
recognization_list = {}

for j, file in enumerate(files):
    harvard = sr.AudioFile(file)
    filename_save = f"{path_save}/{file.split('/')[-1]}.json"

    if(os.path.exists(filename_save)):
        print(f"{filename_save} already exists")
        continue

    recognization_list = {}
    recognization_list[file] = {"data": "", "duration": 0}

    indexOfEmptyResponse = 0
    for i in range(int(length / term)):

        try:
            with harvard as source:
                print(file, i, '/ %s' %(length/term))
                # r.adjust_for_ambient_noise(source)
                audio = r.record(source, offset = i*term, duration = term )
                a = r.recognize_google(audio, language = 'ko-KR', show_all = True)
                if(a== []):
                    indexOfEmptyResponse +=1
                    if(indexOfEmptyResponse > 720):
                        break
                    continue
                print(a);
                recognization_list[file]['data'] += " " + a['alternative'][0]['transcript']
                recognization_list[file]['duration'] = i*5/60
        except:
            break

    with open(f"{path_save}/{file.split('/')[-1]}.json", "w", encoding='UTF-8-sig') as output:
        output.write(json.dumps(recognization_list[file], ensure_ascii=False))

#
# print(recognization_list)
#
# for j, entry in enumerate(recognization_list):
#     print(entry, recognization_list[entry])
#     with open(f"/Volumes/T7/auto diary/pythonProject/dataAnalyzed/phoneCall/{entry.split('/')[-1]}.json", "w", encoding = 'UTF-8-sig') as file:
#         file.write(json.dumps(recognization_list[entry], ensure_ascii=False))