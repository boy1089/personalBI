


from pydub import AudioSegment
import librosa

print('aa')

path =r"/Volumes/T7/auto diary/data/audio/20220731_204726_audio.m4a"
path2 = r'/Volumes/T7/auto diary/data/audio/20221002_223016_audio.m4a'
audio = AudioSegment.from_file(path2)

c = audio.get_array_of_samples()
print('aa')


y, sr = librosa.load(path2)

print(y)
print('aa')
import audioread

with audioread.audio_open(path2) as f:
    totalsec = f.duration
    print(totalsec)

