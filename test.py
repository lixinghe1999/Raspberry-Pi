from bmi160 import bmi160_accsave, bmi160_gyrosave
from multiprocessing import Process
import argparse
import subprocess
import time


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--time', action = "store",type=int, default=5, required=False, help='time of data recording')    
    args = parser.parse_args()

    sample_rate = 1600
    for i in range(10):
        bmi160_accsave('bmiacc', sample_rate, args.time, 0)
        bmi160_accsave('bmiacc', sample_rate, args.time, 1)


