import numpy as np
import librosa, librosa.display 
import matplotlib.pyplot as plt

FIG_SIZE = (15,10)
# load audio file with Librosa

from pydub import AudioSegment
import os
import glob 
import winsound
import time
from matplotlib.animation import FuncAnimation 
import wave
import pyaudio

path = r"D:\python\7. logger2\logger\data\voice"

os.chdir(path)
files = glob.glob('*.m4a')

for i, file in enumerate(files[2:3]):
    m4a_file = file
    wav_filename = file.replace('m4a', 'wav')
        
    track = AudioSegment.from_file(m4a_file,  format= 'm4a')
    file_handle = track.export(wav_filename, format='wav')
    
    
file = file.replace('m4a', 'wav')
sig, sr = librosa.load(file, sr=22050, duration = 60)





fig, ax = plt.subplots() 
xfixdata, yfixdata = 7, 50
xdata = 0
ydata = 0
max_time = 60
# list_var_points = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
list_var_points = np.arange(0, max_time, 0.1)


librosa.display.waveshow(sig, sr, alpha=0.5)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Waveform")
plt.xlim(0, 60)
ln, = plt.plot('ro-', animated=True)

def init(): 
    ax.set_xlim(0, max_time) 
    ax.set_ylim(0, max_time) 
    return ln, 
 
def update(frame): 
    ydata = list_var_points[frame] 
    # (시작선x, 끝선x), (시작선y, 끝선y)
    ln.set_data([ydata,ydata], [yfixdata,xdata])    
    return ln,   


ani = 0
is_ani_running =True


def onClick2(event):
    print(event.xdata, event.ydata)
    global ani
    
    if ani == 0 : 
            
        winsound.PlaySound(file, winsound.SND_FILENAME)
        ani = FuncAnimation(fig, update, 
                            frames=range(int(event.xdata*10), len(list_var_points)),
                            interval = 100,
                            init_func=init, blit=True) 
    else :
        ani._stop()
        winsound.PlaySound(None)
        del ani
        ani = FuncAnimation(fig, update, 
                            frames=range(int(event.xdata*10), len(list_var_points)),
                            interval = 100,
                            init_func=init, blit=True) 
        
fig.canvas.mpl_connect('button_press_event', onClick2)