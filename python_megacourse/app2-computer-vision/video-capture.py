import cv2
import os
import time

# https://www.udemy.com/course/the-python-mega-course/learn/lecture/4775498#content
video = cv2.VideoCapture(0)

check, frame = video.read()

print(check)        # boolean
print(frame.shape)  # 720 x 1280 x 3

video.release()


'''
# Screwing around

time.sleep(3)

check, frame = video.read()

print(check)
cv2.imwrite("webcam-frame.jpg", frame)

video.release()

# Screwing around 2 -- works fine
# converting video to greyscale
while True:
    check, frame = video.read()
    if check == False:
        break
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Grey Converted Webcam", gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):    # ord() is extremely interesting
            video.release()
            break
'''


