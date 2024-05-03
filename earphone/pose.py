import cv2
import time
def record(duration=10):
    # Create a VideoCapture object to capture video from the webcam
    video_capture = cv2.VideoCapture(0)
    # Define the codec and create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # output_file = 'output.avi'
    output_file = 'video/{}.mp4'.format(str(time.time()))
    fps = 30.0  # Frames per second
    frame_size = (640, 480)  # Frame size (width, height)
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, frame_size)
    count = 0
    # Loop until the user presses 'q'
    while True:
        # Capture frame-by-frame from the webcam
        ret, frame = video_capture.read()
        # Write the frame to the video file
        video_writer.write(frame)
        cv2.imshow('Video', frame)

        count += 1
        if count == duration * fps:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the VideoCapture and VideoWriter objects
    video_capture.release()
    video_writer.release()
    # Close all OpenCV windows
    cv2.destroyAllWindows()
if __name__ == '__main__':
    record(-1)