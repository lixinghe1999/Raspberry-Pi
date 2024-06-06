import cv2
import sounddevice as sd
from receive_arduino import record as record_imu
from receive_sounddevice import record as record_audio
def record(output_file, recording_duration=5):
    # # Video settings
    # video_width = 640
    # video_height = 480
    # video_output = output_file + '.mp4'

    # # Initialize video capture
    # video_capture = cv2.VideoCapture(0)
    # video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, video_width)
    # video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, video_height)
    return None

if __name__ == '__main__':
    import argparse
    import datetime
    import multiprocessing
    parser = argparse.ArgumentParser(description='Record audio and video')
    parser.add_argument('--sensors', '-s', default=['earphone', 'micarray'], nargs='+', required=False)
    parser.add_argument('--duration', '-d', default=5, type=int, required=False)

    args = parser.parse_args()
    output_file = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    func_list = []
    for sensor in args.sensors:
        if sensor == 'earphone':
            func_list.append([record_audio, (output_file + '_earphone', 1, 2, args.duration)])
        elif sensor == 'micarray':
            func_list.append([record_audio, (output_file + '_micarray', 2, 8, args.duration)])
        elif sensor == 'imu':
            func_list.append(record_imu)
        else:
            func_list.append(record)
    
    multiprocessing.Pool(len(func_list)).map(lambda x: x[0](*x[1]), func_list)
