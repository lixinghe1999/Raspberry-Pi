import os
import numpy as np
from scipy import signal
import librosa
import matplotlib.pyplot as plt

if __name__ == "__main__":
    b1, a1 = signal.butter(4, 800, 'lowpass', fs=8000)
    b2, a2 = signal.butter(4, 80, 'highpass', fs=1600)

    target_folder = ['AM']
    for folder in target_folder:
        files = os.listdir(folder)
        if files[0] == '.DS_Store': # For macOS
            files = files[1:]
        for i in range(len(files)//2):
            print(mic_f, acc_f)
            mic_f = files[1 + i*2]
            acc_f = files[0 + i*2]

            mic, sr = librosa.load(os.path.join(folder, mic_f), sr=None, mono=True)
            print(mic.shape, sr)
            mic = signal.filtfilt(b1, a1, mic)[::5]

            acc, sr = librosa.load(os.path.join(folder, acc_f), sr=None, mono=False) 
            print(acc.shape, sr)
            acc = signal.filtfilt(b2, a2, acc, axis=1)
            
            for i in range(3):
                acc[i, :] = signal.wiener(acc[i, :], 12)
    
            f, t, mic_spec = signal.spectrogram(mic, fs=1600, nperseg=64, noverlap=32, nfft=64, window='hann', 
                                                scaling='spectrum', mode='magnitude')
            f, t, acc_spec = signal.spectrogram(acc, axis=1, fs=1600, nperseg=64, noverlap=32, nfft=64, window='hann', 
                                                scaling='spectrum', mode='magnitude')
            
            fig, axs = plt.subplots(5,2)
            plt.subplots_adjust(wspace=0.05, hspace=0.05)
            fig.tight_layout()
            for i in range(3):
                axs[i][0].imshow(acc_spec[i, :]) 
            axs[3][0].imshow(np.mean(acc_spec, axis=0))
            axs[4][0].imshow(mic_spec)
            plt.show()
        