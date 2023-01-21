import pydub 
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal



def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_file(f, "mp4")
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y
    
x = read(r"/Volumes/T7/auto diary/pythonProject/src/VoiceRecognition/Microphone.mp4")


start_sec = 800
step_sec = 30
samplingRate = x[0]
data = x[1]

data2 = data.T[0][samplingRate * (start_sec):samplingRate *(start_sec + step_sec) ]


f, t, Sxx = signal.spectrogram(data2, samplingRate, nfft = 1024)

Sxx = np.log(Sxx)


plt.pcolormesh(t, f, Sxx, shading='gouraud')
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()

import speech_recognition as sr
r = sr.Recognizer()
jackhammer = sr.AudioFile(r'/Volumes/T7/auto diary/pythonProject/data/audio/20220807_110035_audio.m4a')
with jackhammer as source:
    audio = r.record(source)
r.recognize_google(audio)


print('a')