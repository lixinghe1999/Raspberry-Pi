import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
# Parameters
total_duration = 1.0  # Total duration of the signal in seconds
pulse_duration = 0.04  # Duration of each pulse in seconds
pulse_interval = 0.0  # Time interval between pulses in seconds
sample_rate = 48000  # Sample rate in Hz
start_freq = 16000  # Starting frequency in Hz
end_freq = 20000  # Ending frequency in Hz

# Calculate the number of pulses
num_pulses = int(total_duration / (pulse_duration + pulse_interval))

# Generate time vector for the entire signal
t = np.linspace(0, total_duration, int(total_duration * sample_rate), endpoint=False)

# Generate the FMCW audio signal
data = np.zeros_like(t)
pulse_time = 0
for _ in range(num_pulses):
    # Calculate the instantaneous frequency for each pulse
    freq = np.linspace(start_freq, end_freq, int(pulse_duration * sample_rate), endpoint=False)
    t = np.linspace(0, pulse_duration, int(pulse_duration * sample_rate), endpoint=False)
    # Generate the FMCW pulse signal
    pulse_signal = np.sin(2 * np.pi * freq * t)
    window = signal.windows.tukey(int(pulse_duration * sample_rate), 0.2, )
    pulse_signal = pulse_signal * window
    # Add the pulse signal to the main signal
    data[int(pulse_time * sample_rate): int(pulse_time * sample_rate)+int(pulse_duration * sample_rate) ] += pulse_signal
    
    # Update the pulse time for the next pulse
    pulse_time += pulse_duration + pulse_interval

# Normalize the signal
data = np.int16(data * 32767)
wavfile.write('FMCW.wav', sample_rate, data)

total_duration = 1.0  # Total duration of the signal in seconds
pulse_duration = 1  # Duration of each pulse in seconds
pulse_interval = 0  # Time interval between pulses in seconds
sample_rate = 48000  # Sample rate in Hz
start_freq = 17000  # Starting frequency in Hz
end_freq = 21000  # Ending frequency in Hz

# Calculate the number of pulses
num_pulses = int(total_duration / (pulse_duration + pulse_interval))

# Generate time vector for the entire signal
t = np.linspace(0, total_duration, int(total_duration * sample_rate), endpoint=False)

# Generate the FMCW audio signal
data = np.zeros_like(t)
pulse_time = 0
for _ in range(num_pulses):
    # Calculate the instantaneous frequency for each pulse
    freq = np.linspace(start_freq, end_freq, int(pulse_duration * sample_rate), endpoint=False)
    t = np.linspace(0, pulse_duration, int(pulse_duration * sample_rate), endpoint=False)
    # Generate the FMCW pulse signal
    pulse_signal = np.sin(2 * np.pi * freq * t)
    # window = signal.windows.tukey(int(pulse_duration * sample_rate), 0.2, )
    # pulse_signal = pulse_signal * window
    # Add the pulse signal to the main signal
    data[int(pulse_time * sample_rate): int(pulse_time * sample_rate)+int(pulse_duration * sample_rate)] += pulse_signal
    
    # Update the pulse time for the next pulse
    pulse_time += pulse_duration + pulse_interval

# Normalize the signal
data = np.int16(data * 32767)
wavfile.write('CW.wav', sample_rate, data)