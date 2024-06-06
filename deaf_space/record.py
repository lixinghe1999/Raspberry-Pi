import sounddevice as sd
# from receive_arduino import record as record_imu
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
    from multiprocessing import Process
    parser = argparse.ArgumentParser(description='Record audio and video')
    parser.add_argument('--sensors', '-s', default=['earphone', 'micarray'], nargs='+', required=False)
    parser.add_argument('--duration', '-d', default=5, type=int, required=False)

    args = parser.parse_args()
    output_file = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    process_list = []
    for sensor in args.sensors:
        if sensor == 'earphone':
            p = Process(target=record_audio, args=(output_file + '_earphone', 1, 2, args.duration))
            process_list.append(p)
        elif sensor == 'micarray':
            p = Process(target=record_audio, args=(output_file + '_micarray', 2, 8, args.duration))
            process_list.append(p)
        else:
            pass
    for p in process_list:
        p.start()
    for p in process_list:
        p.join()