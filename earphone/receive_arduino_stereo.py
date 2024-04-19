from receive_arduino import *
from multiprocessing import Process

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--time', '-t', action = "store", type=int, default=2, required=False, help='time of data recording')    
    parser.add_argument('--sensor', '-s', action = "store", type=str, default='A', required=False, help='A, M or AM')    
    parser.add_argument('--port', '-p', action = "store", nargs='+', type=str, default='COM9 COM10', required=False, help='serial port name')
    # "/dev/ttyACM0" for linux
    # "/dev/cu.usbmodem1401" for mac os
    args = parser.parse_args()
    print(args.port)
    if args.sensor == 'A':
        sample_rate = 800
        channel = 3
        p1 = Process(target=record, args=(args.port[0], sample_rate, args.time, channel, args.sensor, True))
        p2 = Process(target=record, args=(args.port[1], sample_rate, args.time, channel, args.sensor, True))

        p1.start()
        p2.start()
        p1.join()
        p2.join()
    # elif args.sensor == 'M':
    #     sample_rate = 8000
    #     channel = 1
    #     record(args.port, sample_rate, args.time, channel, args.sensor, True)
    # else: # sensor = 'AM'
    #     sample_rate = [1600, 8000]
    #     channel = [3, 1]        
    #     simultaneous_record(args.port, sample_rate, args.time, channel, 'AM', True)