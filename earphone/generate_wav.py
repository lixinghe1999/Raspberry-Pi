import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
# Parameters
total_duration = 2  # Total duration of the signal in seconds
pulse_duration = 2 # Duration of each pulse in seconds
pulse_interval = 0.0  # Time interval between pulses in seconds
sample_rate = 48000  # Sample rate in Hz
start_freq = [20, ]  # Starting frequency in Hz
end_freq = [20000]  # Ending frequency in Hz


assert len(start_freq) == len(end_freq)
t = np.linspace(0, pulse_duration, int(pulse_duration * sample_rate))
chirps = []
for s_freq, e_freq in zip(start_freq, end_freq):
    chirp = signal.chirp(t, s_freq, pulse_duration, e_freq, method='linear')
    interval = np.zeros(int(pulse_interval * sample_rate))
    chirp = np.concatenate((chirp, interval))
    chirps.append(chirp)
chirp = np.stack(chirps)
print(chirp.shape)

data = np.zeros((len(start_freq), int(total_duration * sample_rate), ))
num_pulse = int(total_duration / (pulse_duration + pulse_interval))
print(num_pulse)
for i in range(num_pulse):
    start_idx = int(i * (pulse_duration + pulse_interval) * sample_rate)
    end_idx = int((i + 1) * (pulse_duration + pulse_interval) * sample_rate)
    data[:, start_idx:end_idx] = chirp
wavfile.write('fmcw.wav', sample_rate, data.T)