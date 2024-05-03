'''
we use this script to visualize our results
'''
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import matplotlib.animation as animation

def sync_two_IMUs(l, r, seq_len=500):
    left_time = float(l.split('_')[0])
    right_time = float(r.split('_')[0])

    left_imu = np.load('A_left/' + l)
    right_imu = np.load('A_right/' + r)
    resampled_left = signal.resample(left_imu, seq_len)
    resampled_right = signal.resample(right_imu, seq_len)

    if left_time < right_time:
        left_offset = right_time - left_time
        resampled_right = np.concatenate((np.zeros((int(left_offset), 6)), resampled_left), axis=0)
        resampled_right = resampled_right[:seq_len]
        sync_time = left_time
    else:
        right_offset = left_time - right_time
        resampled_left = np.concatenate((np.zeros((int(right_offset), 6)), resampled_right), axis=0)
        resampled_left = resampled_left[:seq_len]
        sync_time = right_time
    return resampled_left, resampled_right, sync_time


video_path = '1714281087.1778603.mp4'
cap = cv2.VideoCapture('video/'+video_path)
fps = cap.get(cv2.CAP_PROP_FPS)

video_time = float(video_path[:-4])
left, right = os.listdir('A_left'), os.listdir('A_right')
for l, r in zip(left, right):
    resampled_left, resampled_right, sync_time = sync_two_IMUs(l, r)
    start_offset = int((sync_time - video_time ) * fps)
    end_offset = start_offset + int(5 * fps)
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].set_title('Video')
    axs[0, 1].set_title('Left IMU')
    axs[1, 1].set_title('Right IMU')
    axs[1, 0].remove()
    axs[0, 1].plot(resampled_left)
    axs[1, 1].plot(resampled_right)
    left_timeline = axs[0, 1].plot([0, 0], [-1, 1], color='r')
    right_timeline = axs[1, 1].plot([0, 0], [-1, 1], color='r')
    image_ax = axs[0, 0].imshow(np.zeros((480, 640, 3)))
    axs[0, 0].axis('off')
    def animate(i):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_ax.set_data(frame)
        index_imu = int((i - start_offset) * resampled_left.shape[0] / (end_offset - start_offset))
        left_timeline[0].set_data([index_imu, index_imu], [-10000, 10000])
        right_timeline[0].set_data([index_imu, index_imu], [-10000, 10000])
    myAnimation = animation.FuncAnimation(fig, animate, frames=range(start_offset, end_offset), \
                                      interval=1/fps, blit=False, repeat=False)
    # plt.show()
    myAnimation.save('preview.gif', fps=fps)
    break