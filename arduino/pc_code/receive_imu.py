# Progetto di Tesi su:
# Classificazione su base audio del traffico con algoritmi di TinyML su dispositivi embedded
# Autore: Francesco Maccantelli
# Data: 20/05/2022
# Università degli Studi di Siena
# Software per creazione TrainingSet - Registrazione audio

""" 
  _____                            _   
 |_   _|                          | |  
   | |  _ __ ___  _ __   ___  _ __| |_ 
   | | | '_ ` _ \| '_ \ / _ \| '__| __|
  _| |_| | | | | | |_) | (_) | |  | |_ 
 |_____|_| |_| |_| .__/ \___/|_|   \__|
                 | |                   
                 |_|                    """

import serial
import sys
import time
from struct import unpack
import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt



""" 
  _____                               _                
 |  __ \                             | |               
 | |__) |_ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __ ___ 
 |  ___/ _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__/ __|
 | |  | (_| | | | (_| | | | | | |  __/ ||  __/ |  \__ \
 |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|  |___/
                                                       
 """    

def record_audio_wav(time_stamp,serial_port_name, sample_rate=800, sample_length=5): 
    print("Start audio recording...")
    ser = serial.Serial(serial_port_name, 115200, timeout=None)     # Create Serial link
    data = bytearray()
    samples = int(sample_rate * sample_length)
    start_time = time.time()
    for i in range(samples):
      #ser.read_until()
      c = ser.read(2)
      data.extend(c)
    print("Stop audio recording.")
    print("real sample rate:", i/(time.time()-start_time), 'expect sample rate:', sample_rate)
    data = unpack('H'*(len(data)//2), data)
    data = np.array(data, dtype=np.int32)/(32768.0*2)
    print(data.shape, np.max(data), np.min(data))
    write("audio/" + time_stamp + ".wav", sample_rate, data.astype(np.float32))
    ser.close() 
    plt.plot(data)
    plt.show()


if __name__ == '__main__':
    #Importing sys parameters
    
  par_time_stamp = str(time.time())
  par_sample_length = 5
  if sys.argv[1] == "linux":
      par_serial_port_name = "/dev/ttyACM0"
  elif sys.argv[1] == "win":
      par_serial_port_name = "COM5"
    
  record_audio_wav(par_time_stamp,par_serial_port_name, 800, par_sample_length)