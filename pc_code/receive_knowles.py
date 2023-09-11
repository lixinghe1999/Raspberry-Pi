'''
This script read the data from the Knowles V2S200D evaluation kit
'''
import sounddevice as sd
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import librosa
import time

fs = 48000  # Sample rate

def start():
    global myrecording
    myrecording = sd.rec(int(20 * fs), samplerate=fs, channels=2)

def record(fname, duration, plot=False):
    global myrecording
    sd.stop()
    myrecording = myrecording[:fs * duration, :]
    write(fname, fs, myrecording)  # Save as WAV file
    myrecording = myrecording.T
    if plot:
        mel_spec = librosa.feature.melspectrogram(y=myrecording, sr=fs, n_mels=80)
        fig, axs = plt.subplots(2, 2)
        axs[0, 0].plot(myrecording[0, :])
        axs[1, 0].plot(myrecording[1, :])
        axs[0, 1].imshow(mel_spec[0, :])
        axs[1, 1].imshow(mel_spec[1, :])
        plt.show()
if __name__ == '__main__':
    start()
    time.sleep(5)
    print('done')
    record('test.wav', 5, plot=False)