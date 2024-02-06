from scipy.misc import electrocardiogram
import matplotlib.pyplot as plt
import pywt
import numpy as np
ecg = electrocardiogram()


FPData = ecg.reshape(10800,-1)
DWTcoeffs = pywt.wavedec(FPData[:,1], 'db4')
DWTcoeffs[-1] = np.zeros_like(DWTcoeffs[-1])
DWTcoeffs[-2] = np.zeros_like(DWTcoeffs[-2])
DWTcoeffs[-3] = np.zeros_like(DWTcoeffs[-3])
DWTcoeffs[-4] = np.zeros_like(DWTcoeffs[-4])
DWTcoeffs[-5] = np.zeros_like(DWTcoeffs[-5])
DWTcoeffs[-6] = np.zeros_like(DWTcoeffs[-6])
DWTcoeffs[-7] = np.zeros_like(DWTcoeffs[-7])
# DWTcoeffs[-8] = np.zeros_like(DWTcoeffs[-8])
# DWTcoeffs[-9] = np.zeros_like(DWTcoeffs[-9])

filtered_data_dwt=pywt.waverec(DWTcoeffs,'db4',mode='symmetric',axis=-1)
plt.figure(figsize=(15,6))
plt.plot(FPData[:,1],color='red')
plt.plot(filtered_data_dwt, markerfacecolor='none',color='black')
print(FPData[:,1].shape, filtered_data_dwt.shape)
plt.legend(['Real Data', 'Denoised Data'], loc='best')
plt.show()