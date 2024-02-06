import os
from utils.handrate import load_imu, process_imu, show_imu
from utils.flashppg import load_back, process_back, show_back

sensor = 'imu'
folder = './data/' + sensor
func_map = {'imu': {'load': load_imu, 'process': process_imu, 'show': show_imu},
            'imu_chest': {'load': load_imu, 'process': process_imu, 'show': show_imu},
            'back': {'load': load_back, 'process': process_back, 'show': show_back}}
for f in os.listdir(folder):
    print(f)
    f = os.path.join(folder, f)
    data = func_map[sensor]['load'](f)
    data = func_map[sensor]['process'](data)
    func_map[sensor]['show'](data)

