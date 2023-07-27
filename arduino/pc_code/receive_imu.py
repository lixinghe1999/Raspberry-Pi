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




""" 
  _____                               _                
 |  __ \                             | |               
 | |__) |_ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __ ___ 
 |  ___/ _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__/ __|
 | |  | (_| | | | (_| | | | | | |  __/ ||  __/ |  \__ \
 |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|  |___/
                                                       
 """    

def record_audio_wav(time_stamp,serial_port_name,sample_length): 
    print("Start audio recording...")
    ser = serial.Serial(serial_port_name, 115200, timeout=None)     # Create Serial link
    data = bytearray()
    samples = int(476 * sample_length)
    start_time = time.time()
    for x in range(samples):
      ser.read_until()
      cc1 = ser.read(2)
      data.extend(cc1)
    print("Stop audio recording.")
    print("audio:", time.time()-start_time) 
    data = unpack('h'*(len(data)//2), data)
    data = np.array(data, dtype=np.int16) / 32768.0
    write("audio/" + time_stamp + ".wav", 472, data.astype(np.float32))
    ser.close() 


if __name__ == '__main__':
    #Importing sys parameters
    
  par_time_stamp = str(time.time())
  if sys.argv[1] == "linux":
      print("TEST MODE audio !")
      par_serial_port_name = "/dev/ttyACM0"
      par_sample_length = 10
  elif sys.argv[1] == "win":
      print("TEST MODE audio !")
      par_serial_port_name = "COM5"
      par_sample_length = 1
  else:
      par_serial_port_name = str(sys.argv[2])
      par_sample_length = float(sys.argv[3])
    

  #record_audio(par_time_stamp,par_serial_port_name,par_sample_length)
  record_audio_wav(par_time_stamp,par_serial_port_name,par_sample_length)