import os
import numpy as np
from scipy import signal, io, stats
import matplotlib.pyplot as plt

def preprocess(data, shift):
    data = data[:, :-1]
    data = np.roll(data, shift, axis=0)
    data /= 2 ** 14
    b, a = signal.butter(4, 80, 'highpass', fs=1600)
    data = signal.filtfilt(b, a, data, axis=0)
    for i in range(3):
        data[:, i] = signal.wiener(data[:, i], 12)
    # data = np.clip(data, -0.05, 0.05)
    return data
def name2shift(mic_file, imu_file):
    time_mic = float(mic_file.split('_')[0])
    time_imu = float(imu_file.split('_')[0])
    return int((time_imu - time_mic)*1600)
if __name__ == "__main__":
    # os.system('python3 datarecord.py --mode 1')
    folder = 'data'
    files = os.listdir(folder)
    files.sort()
    files = [files[i*3:(i+1)*3] for i in range(len(files)//3)]
    index = 0
    mic_file, imu_file1, imu_file2 = files[index]

    shift1 = name2shift(mic_file, imu_file1)
    shift2 = name2shift(mic_file, imu_file2)
    imu1 = np.loadtxt(os.path.join(folder, imu_file1))
    imu1 = preprocess(imu1, shift1)
    imu2 = np.loadtxt(os.path.join(folder, imu_file2))
    imu2 = preprocess(imu2, shift2)

    sr, audio = io.wavfile.read(os.path.join(folder, mic_file))
    print('finished reading, shift:', shift1, shift2, ',shape:', imu1.shape, imu2.shape, audio.shape)
    b, a = signal.butter(4, 800, 'lowpass', fs=16000)
    audio = signal.filtfilt(b, a, audio)
    audio_downsample = audio[::10]
   
    for i in range(3):
        correlate1 = stats.pearsonr(imu1[:, i], audio_downsample)
        correlate2 = stats.pearsonr(imu2[:, i], audio_downsample)
        print(correlate1, correlate2)
 
    f, t, imu1_spec = signal.spectrogram(imu1, axis=0, fs=1600, nperseg=64, noverlap=32, nfft=64, window='hann', 
                                        scaling='spectrum', mode='magnitude')
    f, t, imu2_spec = signal.spectrogram(imu2, axis=0, fs=1600, nperseg=64, noverlap=32, nfft=64, window='hann', 
                                        scaling='spectrum', mode='magnitude')
    f, t, audio_spec = signal.spectrogram(audio_downsample, fs=1600, nperseg=64, noverlap=32, nfft=64, window='hann', 
                                        scaling='spectrum', mode='magnitude')
    fig, axs = plt.subplots(5, 2)
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    fig.tight_layout()
    for i in range(3):
        axs[i][0].imshow(imu1_spec[:, i])      
        axs[i][1].imshow(imu2_spec[:, i])
    imu1_spec = np.mean(imu1_spec, axis=1)
    imu2_spec = np.mean(imu2_spec, axis=1)
    axs[3][0].imshow(imu1_spec)
    axs[3][1].imshow(imu2_spec)
    plt.subplot(515)
    plt.imshow(audio_spec)
    # axs[2].imshow(audio_spec)
    # plt.show()
    plt.savefig('plot.png')
    