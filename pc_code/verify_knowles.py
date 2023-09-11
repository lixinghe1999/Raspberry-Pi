'''
This script read the data from the Knowles V2S200D evaluation kit
'''
import matplotlib.pyplot as plt
import librosa
import numpy as np

def stats_metric(recording):
    import scipy.stats
    metric1 = scipy.stats.pearsonr(recording[0], recording[1])    # Pearson's r
    metric2 = scipy.stats.spearmanr(recording[0], recording[1])   # Spearman's rho
    metric3 = scipy.stats.kendalltau(recording[0], recording[1])  # Kendall's tau
    metric4 = np.mean(np.abs(recording), axis=-1)        # Mean absolute error
    print(metric1, metric2, metric3, metric4)
fs = 48000  # Sample rate
seconds = 30  # Duration of recording
in_ear, sr = librosa.load('in-ear.wav', sr=None, mono=False)
out_ear, sr = librosa.load('out-ear.wav', sr=None, mono=False)
stats_metric(in_ear)
stats_metric(out_ear)

