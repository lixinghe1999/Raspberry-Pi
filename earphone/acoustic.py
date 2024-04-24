import sounddevice as sd
import scipy.io.wavfile as wavfile
from scipy import signal
import matplotlib.pyplot as plt

def play_and_rec(file='fmcw.wav'):
    rate, wave = wavfile.read(file)
    myrecording = sd.playrec(wave, rate, channels=2 )
    sd.wait()
    wavfile.write('recording.wav', rate, myrecording)

def plot_freqz(file='recording.wav'):
    rate, myrecording = wavfile.read(file)
    frequencies, response_left = signal.freqz(myrecording[:, 0], fs=rate)
    frequencies, response_right = signal.freqz(myrecording[:, 1], fs=rate)

    fig, axs = plt.subplots(3, 1)
    axs[0].plot(frequencies, abs(response_left))
    axs[0].set_yscale('log')
    axs[1].plot(frequencies, abs(response_right))
    axs[1].set_yscale('log')

    axs[2].plot(frequencies, abs(response_left)/abs(response_right))
    axs[2].plot([0, frequencies[-1]], [1, 1], 'r--')
    axs[2].set_yscale('log')
    plt.savefig('response.png')

if __name__ == '__main__':
    sd.default.device = [1, 0]
    devices = sd.query_devices()
    print(devices)
    play_and_rec()
    plot_freqz()