import subprocess
import time
import cv2
import numpy as np
from spotify import Spotify

def is_green_frame(frame):
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the turquoise color
    lower = np.array([70, 100, 100])
    upper = np.array([90, 255, 255])

    # Threshold the frame to get only the turquoise pixels
    mask = cv2.inRange(hsv, lower, upper)

    # Count the number of turquoise pixels in the frame
    count = cv2.countNonZero(mask)

    # If there are turquoise pixels in the frame, return True, else False
    if count > 0:
        return True
    else:
        return False

def check():
    devices = []
    output = subprocess.check_output(['system_profiler', 'SPAudioDataType']).decode()
    for line in output.split('\n'):
        if 'External Microphone' in line:
            device_name = line.split(': ')[-1].strip()
            devices.append(device_name)

    if len(devices) != 0:
        cap = cv2.VideoCapture(0)  # Use 0 for default camera, 1 for external camera
        frame_count = 0
        sp = Spotify()
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            frame_count += 1

            # Display the resulting frame
            cv2.imshow('Video feed', frame)

            # Wait for key press
            key = cv2.waitKey(1)

            # Check if external microphone is still connected
            devices = []
            output = subprocess.check_output(['system_profiler', 'SPAudioDataType']).decode()
            for line in output.split('\n'):
                if 'External Microphone' in line:
                    device_name = line.split(': ')[-1].strip()
                    devices.append(device_name)
            if len(devices) == 0:
                break
            if frame_count != 1:
                if not is_green_frame(frame):
                    if sp.isPlaying():
                        sp.pauseSong()
                else:
                    if not sp.isPlaying():
                        sp.playSong()

                

        # Release the capture and close the window
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    check()
