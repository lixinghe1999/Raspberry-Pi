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

def record(serial_port_name, sample_rate=800, sample_length=5, channel=1, sensor='A', plot=False): 
    '''
    This function records data from serial port and save it as a wav file.
    '''
    ser = serial.Serial(serial_port_name, 115200, timeout=1)     # Create Serial link
    time.sleep(0.5) # important! allow some time for the Arduino to fully reset
    data = bytearray()
    samples = int(sample_rate * sample_length)
    print("try one sample...")
    c = ser.read(2)
    if len(c) == 0:
      print("No data received. Check serial port name.")
      return

    print("Start recording...")
    start_time = time.time()
    for i in range(samples):
      c = ser.read(2 * channel)
      data.extend(c)
    print("Stop imu recording.")
    print("real sample rate:", i/(time.time()-start_time), 'expect sample rate:', sample_rate)
    data = unpack('h'*(len(data)//2), data)
    data = np.array(data, dtype=np.int16).reshape(-1, channel)
    write(sensor + '/' + str(start_time) + ".wav", sample_rate, data)
    ser.close() 
    if plot:
        plt.plot(data)
        plt.show()

def simultaneous_record(serial_port_name, sample_rate=800, sample_length=5, channel=1, sensor='A', plot=False): 
    '''
    This function records data from serial port and save it as a wav file.
    '''
    ser = serial.Serial(serial_port_name, 115200, timeout=1)     # Create Serial link
    time.sleep(0.5) # important! allow some time for the Arduino to fully reset
    data = bytearray()
    samples = int(sample_rate * sample_length)
    print("try one sample...")
    c = ser.read(2)
    if len(c) == 0:
      print("No data received. Check serial port name.")
      return

    print("Start recording...")
    start_time = time.time()
    for i in range(samples):
      c = ser.read(2 * channel)
      data.extend(c)
    print("Stop imu recording.")
    print("real sample rate:", i/(time.time()-start_time), 'expect sample rate:', sample_rate)
    data = unpack('h'*(len(data)//2), data)
    data = np.array(data, dtype=np.int16).reshape(-1, channel)
    write(sensor + '/' + str(start_time) + ".wav", sample_rate, data)
    ser.close() 
    if plot:
        plt.plot(data)
        plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--time', '-t', action = "store", type=int, default=5, required=False, help='time of data recording')    
    parser.add_argument('--sensor', '-s', action = "store", type=str, default='A', required=False, help='A, M or AM')    
    parser.add_argument('--port', '-p', action = "store", type=str, default='COM11', required=False, help='serial port name')
    # "/dev/ttyACM0" for linux??
    args = parser.parse_args()
    if args.sensor == 'A':
        sample_rate = 1600
        channel = 3
    elif args.sensor == 'M':
        sample_rate = 8000
        channel = 1
        
    record(args.port, sample_rate, args.time, channel, args.sensor, True)