'''
Keep those the same as "generate_wav.py"
'''
total_duration = 1.0  # Total duration of the signal in seconds
pulse_duration = 0.04  # Duration of each pulse in seconds
pulse_interval = 0.00  # Time interval between pulses in seconds
sample_rate = 48000  # Sample rate in Hz
start_freq = 16000  # Starting frequency in Hz
end_freq = 20000  # Ending frequency in Hz

vs = 340
period = int(sample_rate * (pulse_duration + pulse_interval))
chirp_len = int(sample_rate * pulse_duration)
bandwidth = end_freq - start_freq
max_frame = 10
dist_min = 0.1
dist_max = 1
range_fft_size = int(10 * sample_rate * pulse_duration)
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt

def load_mic(fname):
    rate, data = wavfile.read(fname)
    assert rate == sample_rate
    data = data / 32767
    print(data.shape)
    # rate, ref = wavfile.read('FMCW.wav')
    ref = signal.chirp(np.linspace(0, pulse_duration, chirp_len), start_freq, pulse_duration, end_freq)
    correlation = np.correlate(data, ref, "valid")
    delay = np.argmax(correlation)
    print(delay)
    delay = 8240
    # plt.subplot(2, 1, 1)
    # plt.plot(data[:int(total_duration * sample_rate)])
    # plt.subplot(2, 1, 2)
    # plt.plot(data[delay: delay + int(total_duration * sample_rate)])    
    # plt.show()
    data = data[delay: delay + int(total_duration * sample_rate)]
    return data
    

def process_mic(data):
    ref = signal.chirp(np.linspace(0, pulse_duration, chirp_len), start_freq, pulse_duration, end_freq)

    low_freq = dist_min * 2 / vs / pulse_duration * bandwidth
    high_freq = dist_max * 2 / vs / pulse_duration * bandwidth
    b, a = signal.butter(5, [low_freq, high_freq], 'bandpass', fs=sample_rate)
    h = signal.firwin(100, [low_freq, high_freq], pass_zero=False, fs=sample_rate)
    print(low_freq, high_freq)
    range_search = np.linspace(0, sample_rate//2, range_fft_size//2) * vs * pulse_duration/ 2 / bandwidth
    range_index = np.logical_and(range_search > dist_min, range_search < dist_max)
    range_search = range_search[range_index]

    range_ffts = []
    delay = 0
    for i in range(max_frame):
        receive_signal = data[delay: delay + chirp_len]
        mix_signal = receive_signal * ref
        mix_signal = signal.lfilter(h, 1, mix_signal)
        # mix_signal = signal.filtfilt(b, a, mix_signal)
        range_fft = np.fft.fft(mix_signal, range_fft_size)[:range_fft_size//2]
        range_fft = np.abs(range_fft[range_index])**2/range_fft_size
        range_ffts.append(range_fft)
        delay += period
        plt.subplot(3, 1, 1)
        plt.plot(receive_signal)
        plt.subplot(3, 1, 2)
        plt.plot(mix_signal)
        plt.subplot(3, 1, 3)
        plt.plot(range_search, range_fft)
        plt.show()
        break
    range_ffts = np.array(range_ffts)
    print(range_ffts.shape, range_search.shape)
    return range_ffts
def show_mic(data):
    
    return