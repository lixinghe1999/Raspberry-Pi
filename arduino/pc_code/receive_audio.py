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

def record_audio_wav(serial_port_name,sample_length): 
    ser = serial.Serial(serial_port_name, 115200, timeout=1)     # Create Serial link
    time.sleep(0.5) # important! allow some time for the Arduino to fully reset
    data = bytearray()
    samples = int(16000 * sample_length)
    print("try one sample...")
    c = ser.read(2)
    if len(c) == 0:
      print("No data received. Check serial port name.")
      return
    
    print("Start audio recording...")
    start_time = time.time()
    for x in range(samples):
      c = ser.read(2)
      data.extend(c)
    print("Stop audio recording.")
    print("audio:", time.time()-start_time) 
    data = unpack('h'*(len(data)//2), data)
    data = np.array(data, dtype=np.int16)
    write("audio/" + str(start_time) + ".wav", 16000, data)
    ser.close() 


if __name__ == '__main__':
  par_sample_length = 5
  if sys.argv[1] == "linux":
      par_serial_port_name = "/dev/ttyACM0"
  elif sys.argv[1] == "win":
      par_serial_port_name = "COM11"
  
  #record_audio(par_time_stamp,par_serial_port_name,par_sample_length)
  record_audio_wav(par_serial_port_name,par_sample_length)