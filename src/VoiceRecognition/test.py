import speech_recognition as sr
import glob
import os

from pydub import AudioSegment
from pydub.playback import play


r = sr.Recognizer()


path = r"D:\python\7. logger2\logger\data\voice"


num = 0
files = glob.glob(os.path.join(path, '*.wav'))
harvard = sr.AudioFile(files[num])
print(files[num])
# song = AudioSegment.from_wav(files[num])
# play(song)


with harvard as source:
    # audio = r.record(source, offset = 3600, duration = 30)
    # audio = r.record(source)
    # r.adjust_for_ambient_noise(source)
    audio = r.record(source, offset = 20, duration = 60 )

a = r.recognize_google(audio, language = 'ko-KR', show_all = False)

print(a)
