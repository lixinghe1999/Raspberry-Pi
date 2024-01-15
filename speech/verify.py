'''
This script read the data from the Knowles V2S200D evaluation kit
'''
import librosa
import numpy as np

def stats_metric(fname):
    recording, sr = librosa.load(fname, sr=None, mono=False)
    import scipy.stats
    metric1 = scipy.stats.pearsonr(recording[0], recording[1]).statistic    # Pearson's r
    metric2 = scipy.stats.spearmanr(recording[0], recording[1]).statistic    # Spearman's rho
    metric3 = scipy.stats.kendalltau(recording[0], recording[1]).statistic   # Kendall's tau
    metric4 = np.mean(np.abs(recording[0] - recording[1]), axis=-1)        # Mean absolute error
    print(metric1, metric2, metric3, metric4)
