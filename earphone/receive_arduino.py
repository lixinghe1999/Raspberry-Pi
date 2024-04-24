'''
Receive data from serial
'''

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
import time
from struct import unpack
import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import argparse



""" 
  _____                               _                
 |  __ \                             | |               
 | |__) |_ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __ ___ 
 |  ___/ _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__/ __|
 | |  | (_| | | | (_| | | | | | |  __/ ||  __/ |  \__ \
 |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|  |___/
                                                       
 """    
def record(serial_port_name, sample_rate=800, sample_length=5, channel=1, sensor='A', plot=False, format='numpy'): 
    '''
    This function records data from serial port and save it as a wav file.
    '''
    ser = serial.Serial(serial_port_name, 115200, timeout=1)     # Create Serial link
    time.sleep(0.2) # important! allow some time for the Arduino to fully reset
    data = bytearray()
    samples = int(sample_rate * sample_length)
    print("try one sample...")
    c = ser.read(2)
    if len(c) == 0:
      print("No data received. Check serial port name.")
      return

    print("Start recording...")
    start_time = time.time()
    ser.flush() # clear buffer
    for i in range(samples):
      c = ser.read(2 * channel)
      data.extend(c)
    print("Stop recording.")
    real_sample_rate = samples/(time.time()-start_time)
    print("real sample rate:", real_sample_rate, 'expect sample rate:', sample_rate)
    data = unpack('h'*(len(data)//2), data)
    data = np.array(data, dtype=np.int16).reshape(-1, channel)

    save_name = sensor + '/' + str(start_time) + "_" + str(int(real_sample_rate))
    if format == 'numpy':
        np.save(save_name + ".npy", data)
    else:
        write(save_name + ".wav", sample_rate, data)
    ser.close() 
    if plot:
        if channel == 3:
          plt.plot(data)
          plt.show()
        else:
          fig, axs = plt.subplots(2, 1)
          axs[0].plot(data[:,:3])
          axs[1].plot(data[:,3:])
          plt.show()

def simultaneous_record(serial_port_name, sample_rate=[1600, 8000], sample_length=5, channel=[3, 1], sensor='AM', plot=False): 
    '''
    This function records data from serial port and save it as a wav file.
    '''
    ser = serial.Serial(serial_port_name, 115200, timeout=1)     # Create Serial link
    time.sleep(0.5) # important! allow some time for the Arduino to fully reset
    data = [bytearray(), bytearray()]
    samples = [int(sr * sample_length) for sr in sample_rate]
    buffer = [192, 512]
    print("try one sample...")
    c = ser.read(2)
    if len(c) == 0:
      print("No data received. Check serial port name.")
      return

    print("Start recording...")
    start_time = time.time()
    i = 0; j = 0
    while (i <= samples[0] or j <= samples[1]):
      ser.read_until()
      id = ser.read(1)
      if id == b'\x00':
        c = ser.read(buffer[0])
        i += len(c)//6
        data[0].extend(c)
      elif id == b'\x01':
        c = ser.read(buffer[1])
        j += len(c)//2
        data[1].extend(c)
    print("Stop recording.")
    print("real sample rate:", [i/(time.time()-start_time), j/(time.time()-start_time)], 'expect sample rate:', sample_rate)
    for i in range(2):
      data[i] = unpack('h'*(len(data[i])//2), data[i])
      data[i]  = np.array(data[i] , dtype=np.int16).reshape(-1, channel[i])
    if args.format == 'numpy':
          np.save(sensor + '/A_' + str(start_time) + ".npy", data[0])
          np.save(sensor + '/M_' + str(start_time) + ".npy", data[1])
    else:
          write(sensor + '/A_' + str(start_time) + ".wav", sample_rate[0], data[0])
          write(sensor + '/M_' + str(start_time) + ".wav", sample_rate[1], data[1])
    ser.close() 
    if plot:
        fig, axs = plt.subplots(2, 1)
        axs[0].plot(data[0])
        axs[1].plot(data[1])
        plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--time', '-t', action = "store", type=int, default=5, required=False, help='time of data recording')    
    parser.add_argument('--sensor', '-s', action = "store", type=str, default='A', required=False, help='A, M or AM')    
    parser.add_argument('--port', '-p', action = "store", type=str, default='COM13', required=False, help='serial port name')
    parser.add_argument('--format', '-f', action = "store", type=str, default='numpy', choices=['numpy', 'wav'], required=False)

    # "/dev/ttyACM0" for linux
    # "/dev/cu.usbmodem1401" for mac os
    args = parser.parse_args()
    if args.sensor == 'A':
        sample_rate = 104
        channel = 6
        record(args.port, sample_rate, args.time, channel, args.sensor, True, args.format)
    elif args.sensor == 'M':
        sample_rate = 8000
        channel = 1
        record(args.port, sample_rate, args.time, channel, args.sensor, True, args.format)
    else: # sensor = 'AM'
        sample_rate = [1600, 8000]
        channel = [3, 1]        
        simultaneous_record(args.port, sample_rate, args.time, channel, 'AM', True, args.format)
    