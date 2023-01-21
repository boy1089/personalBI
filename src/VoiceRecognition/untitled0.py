import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
audio_path = '1.wav'
y, sr = librosa.load(audio_path)

stft_result = librosa.stft(y, n_fft=4096, win_length = 4096, hop_length=1024)
D = np.abs(stft_result)
S_dB = librosa.power_to_db(D, ref=np.max)
librosa.display.specshow(S_dB, sr=sr, hop_length = 1024, y_axis='linear', x_axis='time')
plt.show()

