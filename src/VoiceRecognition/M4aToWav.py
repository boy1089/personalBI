

import sys
# sys.path.append(r"/Users/jiyoung/Downloads/ffmpeg-2022-12-04-git-6c814093d8-full_build/bin/ffprobe")
# sys.path.append(r"/Users/jiyoung/Downloads/ffmpeg-2022-12-04-git-6c814093d8-full_build/bin/ffprobe.exe")
# sys.path.append(r"/Users/jiyoung/Downloads/ffmpeg-2022-12-04-git-6c814093d8-full_build/bin")
# sys.path.append(r"/Volumes/T7/auto diary/pythonProject/src/VoiceRecognition")
# sys.path.append(r"/Volumes/T7/auto diary/pythonProject/src/VoiceRecognition/ffprobe")
# sys.path.append(r"/Volumes/T7/auto diary/pythonProject/src/VoiceRecognition/ffprobe")

print(sys.path)
# import ffmpeg
import os
print(os.environ['PATH'])
os.environ["PATH"] += os.pathsep + r"/Volumes/T7/auto diary/pythonProject/src/VoiceRecognition"
# os.environ["PATH"] += os.pathsep + r"/Volumes/T7/auto diary/pythonProject/src/VoiceRecognition/ffprobe.exe"

from pydub import AudioSegment
import glob

path = r'/Volumes/T7/auto diary/pythonProject/data/phoneCall'
path = r"/Volumes/T7/auto diary/pythonProject/data/audio"

path_json = r"/Volumes/T7/auto diary/pythonProject/dataAnalyzed/audio_term 5sec/*.json"
files_json = glob.glob(path_json)

os.chdir(path)

files = glob.glob('*.m4a')
files.sort()
print(files)

for i, file in enumerate(files):
    print(file)
    file_withoutFormat = file.split('.')[0]
    flagWhetherConvert = True;
    for j, file_json in enumerate(files_json[1:]):
        # print(file_json.find(file))
        if file_json.find(file_withoutFormat) != -1:
            print("file exists ")
            flagWhetherConvert = False
            break

    if flagWhetherConvert:
        m4a_file = file
        print(f'processing {file}')
        wav_filename = file.replace('m4a', 'wav')

        if os.path.exists(wav_filename):
            print(f"{wav_filename} already exists")
            continue

        try :
            track = AudioSegment.from_file(m4a_file,  format= 'm4a')
            file_handle = track.export(wav_filename, format='wav')
        except :
            pass