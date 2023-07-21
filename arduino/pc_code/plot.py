import matplotlib.pyplot as plt
import numpy as np
import json 

file = open( 'audio/test.json','r')
data = json.load(file)['payload']['values']

data = np.array(data)
fft = np.fft.fft(data)
fig, axs = plt.subplots(2)
axs[0].plot(data)
axs[1].plot(fft)
plt.show()
