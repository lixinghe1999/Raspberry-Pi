'''
This script read the data from the Knowles V2S200D evaluation kit
'''
import sounddevice as sd
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import librosa
import time
import threading
import soundfile as sf
stop_event = threading.Event()
fs = 44100  # Sample rate
def select_device():
    name_1 = '1-Microphone'
    name_2 = '2-Microphone'
    devices = sd.query_devices()
    #print(devices)
    for d in devices:
        if name_1 in d['name']:
            device_1 = d['index']
            print(d)
            break
    for d in devices:
        if name_2 in d['name']:
            device_2 = d['index']
            print(d)
            break
    return device_1, device_2
def start_two(device_1, device_2, fname_1, fname_2):
    def record_audio(device, filename):
        # Open the audio file for writing
        with sf.SoundFile(filename, mode='w', samplerate=fs, channels=2, subtype='float') as file:
            def callback(indata, frames, time, status):
                if status:
                    print('Error:', status)
                file.write(indata)
                print(indata.shape, indata.max(), indata.min())
            # Start recording audio until the stop event is set
            with sd.InputStream(device=device, channels=2, callback=callback, blocksize=18000):
                while not stop_event.is_set():
                    pass
    thread1 = threading.Thread(target=record_audio, args=(device_1, fname_1))
    thread2 = threading.Thread(target=record_audio, args=(device_2, fname_2))
    # Start the threads
    thread1.start()
    thread2.start()
    return thread1, thread2
def record_two(thread1, thread2):
    # Set the stop event to stop the recording in both threads
    stop_event.set()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()
    stop_event.clear()
    del thread1, thread2

def start(duration=20):
    global myrecording
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
def record(fname, duration, plot=False):
    global myrecording
    sd.stop()
    myrecording = myrecording[:fs * duration, :]
    write(fname, fs, myrecording)  # Save as WAV file
    if plot:
        myrecording = myrecording.T
        mel_spec = librosa.feature.melspectrogram(y=myrecording, sr=fs, n_mels=80)
        fig, axs = plt.subplots(2, 2)
        axs[0, 0].plot(myrecording[0, :])
        axs[1, 0].plot(myrecording[1, :])
        axs[0, 1].imshow(mel_spec[0, :])
        axs[1, 1].imshow(mel_spec[1, :])
        plt.show()
if __name__ == '__main__':
    # start()
    # time.sleep(5)
    # print('done')
    # record('test.wav', 5, plot=False)

    device_1, device_2 = select_device()
    thread1, thread2 = start_two(device_1, device_2, 'test1.wav', 'test2.wav',)
    time.sleep(2)
    print('done')
    record_two(thread1, thread2)