import cv2
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from receive_arduino import record as record_imu
def record(output_file, recording_duration=5):
    # Video settings
    video_width = 640
    video_height = 480
    video_output = output_file + '.mp4'

    # Audio settings
    audio_channels = 2
    audio_format = 'int16'
    audio_rate = 44100
    audio_frames_per_buffer = 1024
    audio_output = output_file + '.wav'

    # Initialize video capture
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, video_width)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, video_height)

    # Initialize audio recording
    audio_frames = []
    total_audio_frames = int(audio_rate * recording_duration) // audio_frames_per_buffer

    def audio_callback(indata, frames, time, status):
        audio_frames.append(indata.copy())

    # Start audio recording
    audio_stream = sd.InputStream(channels=audio_channels,
                                samplerate=audio_rate,
                                callback=audio_callback)

    audio_stream.start()

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_output, fourcc, 30.0, (video_width, video_height))

    # Recording loop
    while len(audio_frames) < total_audio_frames:
        # Read video frame
        ret, frame = video_capture.read()

        # Write video frame
        video_writer.write(frame)

        # Display the resulting frame
        # cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # Stop audio recording
    audio_stream.stop()

    # Release resources
    video_capture.release()
    video_writer.release()
    cv2.destroyAllWindows()

    # Save audio to file
    audio_data = np.concatenate(audio_frames)
    write(audio_output, audio_rate, audio_data)
if __name__ == '__main__':
    import sys
    import datetime
    if len(sys.argv) < 2:
        record_duration = 5
    else:
        record_duration = int(sys.argv[1])
    output_file = 'dataset/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    record(output_file, record_duration)