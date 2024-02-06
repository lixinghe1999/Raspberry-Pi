import cv2
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
def load_back(file_path):
    # Load video using OpenCV
    cap = cv2.VideoCapture(file_path)

    # Get video properties
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize a numpy array to store the video frames
    video_data = np.zeros((frame_count, frame_height, frame_width, 3), dtype=np.uint8)

    # Read video frames and store in the numpy array
    frame_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        video_data[frame_index] = frame
        frame_index += 1

    # Release the video capture object
    cap.release()
    return video_data
def process_back(video_data):
    red = video_data[:, :, :, 2]
    red_sum = np.sum(red, axis=(1, 2))
    # red_sum = red_sum[20:-5]
    # Apply a moving average filter to the red channel sum
    window_size = 10
    print(red_sum.shape)

    red_sum = red_sum[window_size-1:] - np.convolve(red_sum, np.ones(window_size) / window_size, mode='valid')

    # # apply low pass filter
    # b, a = signal.butter(3, 4, fs=30, btype='low')
    # red_sum = signal.filtfilt(b, a, red_sum)
    # gauss filter

    return red_sum

def show_back(data):
    plt.plot(data)
    plt.show()
    return