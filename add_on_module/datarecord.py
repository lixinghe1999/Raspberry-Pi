
from bmi160 import bmi160_accsave, bmi160_gyrosave
# from mic import open_mic_stream, voice_record, RATE
from multiprocessing import Process
import argparse
import subprocess
import time


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--time', action = "store",type=int, default=5, required=False, help='time of data recording')    
    parser.add_argument('--mode', action = "store",type=int, default=0, required=False, help='with or without microphone')    

    args = parser.parse_args()
    sample_rate = 1600
    if args.mode == 1:
        result = subprocess.check_output('arecord -l', shell=True, encoding='utf-8')
        result = result.split('card ')[1]
        card = int(result[0])
        result = result.split('device ')[1]
        device = int(result[0])
        time_start = time.time()   
        subprocess.call(['arecord', '-D', 'plughw:'+str(card)+','+str(device), '-r', '16000', '-d', str(args.time),
        'mic_' + str(time_start) + '.wav'])
    thread1 = Process(target=bmi160_accsave, args=('bmiacc0', sample_rate, args.time, 0))
    thread2 = Process(target=bmi160_accsave, args=('bmiacc1', sample_rate, args.time, 1))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


