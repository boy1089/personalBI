# -*- coding: utf-8 -*-
import sys, re, glob, ffmpeg

TYPE:str = "wav"
FILE_PATH:str  = ".\*.[Mm][Pp]4"

FILE_PATH:str = r"/Volumes/T7/auto diary/pythonProject/data/phoneCall/*.mp4"

# mp4 -> [mp3][wav] 
def mp4_to_mp3(path,type):
    print(path)
    ffmpeg.run(
        ffmpeg.output(
            ffmpeg.input(path) ,
            re.sub("\.(mp4|MP4)$","."+type,path)
        ))

if ( __name__ == "__main__" ):

    files = glob.glob(FILE_PATH)
    path_json = r"/Volumes/T7/auto diary/pythonProject/dataAnalyzed/audio_term 5sec/*.json"
    files_json = glob.glob(pathÎ_json)
    print(files)
    print(files_json)
    print('aa')
    for i, path in enumerate(files):
        filename = path.split('/')[-1].split('.')[0]
        # mp4_to_mp3(path, TYPE)

