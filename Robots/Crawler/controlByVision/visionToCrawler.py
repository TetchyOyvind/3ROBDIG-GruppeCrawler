#Code based on https://github.com/gmueth/line-following-robot?tab=readme-ov-file

import cv2
import numpy as np
import time
import robotMotion as robot


# Initialize camera
camera = cv2.VideoCapture(0)  # 0 for the first USB cam, 1 for the second, etc.
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 192)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 108)
camera.set(cv2.CAP_PROP_FPS, 20)

robot.initialize()

# Loop over all frames captured by camera indefinitely
while True:
    # Capture frame-by-frame
    ret, image = camera.read()

    # Display camera input
    cv2.imshow('img',image)

    # Create key to break for loop
    key = cv2.waitKey(1) & 0xFF

    # convert to grayscale, gaussian blur, and threshold
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definer omrï¿½det for rï¿½d farge i HSV
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # Lag en maske med den rï¿½de fargen
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find all contours in frame
    contours, hierarchy = cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)

    # Find x-axis centroid of largest contour and cut power to appropriate motor
    # to recenter camera on centroid.
    if len(contours) > 0:
        # Find largest contour area and image moments
        c = max(contours, key = cv2.contourArea)
        M = cv2.moments(c)

        # Find x-axis centroid using image moments
        if M["m00"] != 0:
            cx = int(M['m10']/M['m00'])
        else:
            cx = 0
        if cx >= 150:
            print("Left!")
            robot.autoSteer(-50)

        if cx < 150 and cx > 40:
            print("       Forward!")
            robot.goForward()

        if cx <= 40:
            print("                     Right!")
            robot.autoSteer(50)

    if key == ord("q"):
        break
    
robot.stop()

