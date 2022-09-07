import cv2
import os
import time

# https://www.udemy.com/course/the-python-mega-course/learn/lecture/4775498#content
video = cv2.VideoCapture(0)

# from grepper
while True:
    ret, frame = video.read()
    if not ret:
        break
    else:
        cv2.imshow("live-cam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):    # ord() is extremely interesting
            break
#
#video.release()