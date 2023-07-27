from bmi160 import bmi160_accsave, bmi160_gyrosave
from multiprocessing import Process
import argparse
import subprocess
import time
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--time', action = "store",type=int, default=5, required=False, help='time of data recording')    
    parser.add_argument('--mode', action = "store",type=int, default=0, required=False, help='with or without microphone')    
    parser.add_argument('--dataset', action = "store",type=str, default='data/', required=False, help='path of dataset')    

    args = parser.parse_args()
    sample_rate = 1600
    dataset_path = args.dataset
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)

    if args.mode == 1:
        result = subprocess.check_output('arecord -l', shell=True, encoding='utf-8')
        result = result.split('card ')[1]
        card = int(result[0])
        result = result.split('device ')[1]
        device = int(result[0])
        time_start = time.time()   
        subprocess.Popen(['arecord', '-D', 'plughw:'+str(card)+','+str(device), '-f', 'S16_LE', '-r', '16000', '-d', str(args.time),
         dataset_path + str(time_start) + '_mic' + '.wav'])
    thread1 = Process(target=bmi160_accsave, args=(dataset_path, sample_rate, args.time, 0))
    thread2 = Process(target=bmi160_accsave, args=(dataset_path, sample_rate, args.time, 1))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


