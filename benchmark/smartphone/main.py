import os
from utils.handrate import load_imu, process_imu, show_imu
from utils.flashppg import load_back, process_back, show_back
from utils.acoustic import load_mic, process_mic, show_mic

sensor = 'mic'
folder = './data/' + sensor
func_map = {'imu': {'load': load_imu, 'process': process_imu, 'show': show_imu},
            'back': {'load': load_back, 'process': process_back, 'show': show_back},
            'mic': {'load': load_mic, 'process': process_mic, 'show': show_mic}
            }
for f in os.listdir(folder):
    print(f)
    f = os.path.join(folder, f)
    data = func_map[sensor]['load'](f)
    data = func_map[sensor]['process'](data)
    func_map[sensor]['show'](data)
    break

