import matplotlib.pyplot as plt
import numpy as np
import json 
import os

files = os.listdir('audio')
file = files[-1]
print(file)
f = open('audio/' + file,'r')
data = json.load(f)['payload']['values']

data = np.array(data)
fft = np.abs(np.fft.fft(data))
fig, axs = plt.subplots(2)
axs[0].plot(data)
axs[1].plot(fft)
plt.show()
