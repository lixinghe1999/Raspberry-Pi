# import sounddevice as sd
# # from receive_arduino import record as record_imu
# from receive_sounddevice import record as record_audio
import picamera
def record(output_file, duration):
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.start_recording('{}.h264'.format(output_file))
    camera.wait_recording(duration)
    camera.stop_recording()
if __name__ == '__main__':
    import argparse
    import datetime
    import subprocess
    parser = argparse.ArgumentParser(description='Record audio and video')
    parser.add_argument('--sensors', '-s', default=['earphone', 'micarray'], nargs='+', required=False)
    parser.add_argument('--duration', '-d', default=5, type=int, required=False)

    args = parser.parse_args()
    output_file = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    command_array = 'arecord -Dac108 -f S32_LE -r 16000 -c 8 -d {} {}.wav'.format(args.duration, output_file + '_micarray').split()
    command_earphone = 'arecord -Dhw:1,0 -f S16_LE -r 16000 -c 2 -d {} {}.wav'.format(args.duration, output_file + '_earphone').split()
    subprocess.Popen(command_array)
    subprocess.Popen(command_earphone)
    record(args.duration)

#     from multiprocessing import Process
#    
#     process_list = []
#     for sensor in args.sensors:
#         if sensor == 'earphone':
#             p = Process(target=record_audio, args=(output_file + '_earphone', 1, 2, args.duration))
#             process_list.append(p)
#         elif sensor == 'micarray':
#             p = Process(target=record_audio, args=(output_file + '_micarray', 2, 8, args.duration))
#             process_list.append(p)
#         else:
#             pass
#     for p in process_list:
#         p.start()
#     for p in process_list:
#         p.join()
