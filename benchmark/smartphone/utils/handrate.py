import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import scipy.fft as fft
import pywt
from sklearn.decomposition import PCA

def load_imu(file_path, sr=100):
    def time_stamp_converter(s):
        s = float(s[-6:].replace('_', '.'))
        return s
    with open(file_path, 'rb') as f:
        lines = f.readlines()
    data = np.zeros((len(lines)-1, 7))
    lines = lines[1:]
    for i, line in enumerate(lines):
        line = line.decode('utf-8').strip().split(',')
        data[i, :-1] = list(map(float, line[:-1]))
        data[i, -1] = time_stamp_converter(line[-1])
    data = data[50:, -100:]
    time_stamp = data[:, -1]
    time_stamp -= time_stamp[0]
    time_stamp[time_stamp < 0] += 60
    resample_time = np.arange(0, time_stamp[-1], 1/sr)
    new_data = np.zeros((len(resample_time), 6))
    for i in range(6):
        new_data[:,i] = np.interp(resample_time, time_stamp, data[:, i])
    data = new_data
  
    return data

def process_imu(data, sr=100):
    # threshold = np.mean(np.abs(data), axis=0, keepdims=True)
    # data[np.abs(data) < threshold] = 0
    data = signal.detrend(data, axis=0)
    data /= np.max(np.abs(data), axis=0, keepdims=True)

    pad_num = 100 - data.shape[0] % 100
    data = np.pad(data, ((0, pad_num), (0, 0)), 'constant', constant_values=0)
    
    for i in range(6):
        DWTcoeffs = pywt.wavedec(data[:, i], 'db4')

        # # Estimate the noise standard deviation using the median absolute deviation (MAD)
        # sigma = np.median(np.abs(DWTcoeffs[-1]))
    
        # # Apply soft thresholding to all detail coefficients
        # denoised_coeffs = []
        # for detail_coeff in DWTcoeffs[1:]:
        #     threshold = sigma * np.sqrt(2 * np.log(len(data[:, i])))
        #     denoised_coeffs.append(pywt.threshold(detail_coeff, threshold, mode='soft'))

        DWTcoeffs[-1] = np.zeros_like(DWTcoeffs[-1])
        DWTcoeffs[-2] = np.zeros_like(DWTcoeffs[-2])
        # DWTcoeffs[-3] = np.zeros_like(DWTcoeffs[-3])
        # DWTcoeffs[-4] = np.zeros_like(DWTcoeffs[-4])
        # DWTcoeffs[-5] = np.zeros_like(DWTcoeffs[-5])
        # DWTcoeffs[-6] = np.zeros_like(DWTcoeffs[-6])
        # DWTcoeffs[-7] = np.zeros_like(DWTcoeffs[-7])
        # DWTcoeffs[-8] = np.zeros_like(DWTcoeffs[-8])
        # DWTcoeffs[-9] = np.zeros_like(DWTcoeffs[-9])
        data[:, i] = pywt.waverec(DWTcoeffs,'db4',mode='symmetric')

    # max_point = np.argmax(data, axis=0)
    # for i in range(6):
    #     start = max_point[i]-50 if max_point[i]-50 > 0 else 0
    #     end = start + 100 if start + 100 < len(data) else len(data)
    #     template = data[start: end,i]
    #     cross_corr = signal.correlate(data[:, i], template, mode='same')
    #     data[:, i] = cross_corr

    pca = PCA(n_components=3)
    pca.fit(data[:, :3])
    data[:, :3] = pca.transform(data[:, :3])
    print(pca.explained_variance_ratio_)
    pca.fit(data[:, 3:])
    data[:, 3:] = pca.transform(data[:, 3:])
    print(pca.explained_variance_ratio_)

    return data

def fft_plot(data, ax, sr=100):
    fft_signal = fft.fft(data)
    freqs = fft.fftfreq(len(data), 1 / sr)
    positive_freqs = freqs[:len(freqs)//2]  # Take only the positive frequencies
    positive_fft = fft_signal[:len(freqs)//2]  # Take the corresponding FFT values
    ax.plot(positive_freqs, np.abs(positive_fft))
def cwt_plot(data, ax, sr=100):
    t = np.arange(0, len(data)/sr, 1/sr)
    freqs = np.array([48, 32, 16, 8, 6, 4, 3, 2, 1.5, 1, 0.75, 0.5, 0.25, 0.1,])
    scales = pywt.frequency2scale('morl', freqs/sr)
    coef, freqs = pywt.cwt(data, scales, 'morl', sampling_period=1/sr)
    coef = np.abs(coef)
    ax.pcolormesh(t, freqs, coef, shading='gouraud')
def stft_plot(data, ax, sr=100):
    f, t, spec = signal.stft(data, fs=sr, nperseg=128, noverlap=8, nfft=128, axis=0)
    spec = np.abs(spec)
    ax.pcolormesh(t, f, spec, shading='gouraud')
def show_imu(data):
    fig, axs = plt.subplots(6, 4)
    for i in range(6):
        axs[i, 0].plot(data[:,i])
        fft_plot(data[:,i], axs[i, 1])
        cwt_plot(data[:, i], axs[i, 2])
        stft_plot(data[:, i], axs[i, 3])
    plt.show()
    return 