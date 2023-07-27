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
    samples = int(16000 * sample_length)
    start_time = time.time()
    for x in range(samples):
      ser.read_until()
      cc1 = ser.read(2)
      data.extend(cc1)
    print("Stop audio recording.")
    print("audio:", time.time()-start_time) 
    data = unpack('h'*(len(data)//2), data)
    data = np.array(data, dtype=np.int16)
    write("audio/" + time_stamp + ".wav", 16000, data)
    ser.close() 
def record_audio(time_stamp,serial_port_name,sample_length):

    #TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST

    print("Start audio recording...")


    ser = serial.Serial(serial_port_name, 115200, timeout=None)     # Create Serial link
    file_name = "audio/" + time_stamp + ".json"
    file = open(file_name,"w")
    # Prefix for EdgeImpulse integration
    file.write('{"protected":{"alg":"HS256","ver":"v1"},"signature":"8edcce692f266197144c1ddcbd7a381cf6cbaea4f6433e0b6a765eb7eb7230de","payload":{"device_name":"03:DF:11:CF:64:45","device_type":"ARDUINO_NANO33BLE","interval_ms":0.0625,"sensors":[{"name":"audio","units":"wav"}],"values":[')
    result_ = ""
    result_2 = ""
    samples = int(16000 * sample_length)

    #TEST TEST TEST TEST TEST TEST #TEST TEST TEST TEST TEST TEST
    start_time = time.time()

    for x in range(samples):
      ser.read_until()
      cc1 = ser.read(2)
      res = str(unpack('h'*(1),cc1)[0]) + ','
      # print(cc1, res)
      #res = str(int.from_bytes(cc1, "little"))+","
      result_ += res
      #print(res)
     

    #TEST TEST TEST TEST TEST TEST #TEST TEST TEST TEST TEST TEST
    print("Stop audio recording.")
    print("audio:", time.time()-start_time)  
    #report=open("report.txt","w")
    #report.write("Audio recording: ",time.time()-start_time,"\n")
    
    #report.close()
    file.write(result_)
    
    # Suffix for EdgeImpulse integration
    file.write('0]}}')
    file.close()
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
      par_sample_length = 5
  else:
      par_serial_port_name = str(sys.argv[2])
      par_sample_length = float(sys.argv[3])
    

  #record_audio(par_time_stamp,par_serial_port_name,par_sample_length)
  record_audio_wav(par_time_stamp,par_serial_port_name,par_sample_length)