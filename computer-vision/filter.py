from cv2 import rectangle
import numpy as np
import matplotlib.pyplot as plt
import cv2

eye_cascade = cv2.CascadeClassifier("frontal-eyes35x16.xml")

# interesting pyplot had the base .imread() .imshow() .imwrite() functions
img = plt.imread("webcam-frame.jpg")
#plt.imshow(img) # followed by plt.show()

img.shape
img1 = img.copy()

# This returns the location of the eyes in the format (x,y,w,h). Here
# x stands for the X coordinate of the bottom left corner
# y stands for the Y coordinate of the bottom left corner
# w stands for the width of the eye region
# h stands for the height of the eye region
eye = eye_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)[0]
print(eye)
eye_x,eye_y,eye_w,eye_h = eye
# color is BGR
img = cv2,rectangle(img, (eye_x, eye_y), (eye_x + eye_w, eye_y + eye_h), color = (0,125,125), thickness = 5)

glasses = plt.imread("sample1.png")
glasses = cv2.resize(glasses, (eye_w+50, eye_h+55))
glasses.shape

for i in range(glasses.shape[0]):
    for j in range(glasses.shape[1]):
        if (glasses[i,j,3] > 0):
            # this is a splice
            img1[eye_y + i -  20, eye_x + j - 23, :] = glasses [i,j,: -1]

plt.imshow(img1)
plt.show()
