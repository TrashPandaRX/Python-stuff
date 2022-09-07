import cv2
import os
import numpy as np

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Files")

# had some issues earlier when this was just -> face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") as there was no proper path to this .xml file from app2-computer-vision
face_cascade = cv2.CascadeClassifier(f"{file_path}/haarcascade_frontalface_default.xml")
#img = cv2.imread(os.path.join(file_path, "photo.jpg"))             # easy picture
#img = cv2.imread(os.path.join(file_path, "news.jpg"))              # hard picture
img = cv2.imread(os.path.join(file_path, "istockphoto-451259921-612x612.jpeg"))       # googled picture

# NOTE
# apparently greyscale images are more accurate in detecting faces...whereas color might misidentify faces...
# could this be one aspect as to why some facial recognition software has such a difficult time with people of color, particularly browner-blacker skinned?

gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# scaleFactor = 1.05 means that it will scale down the image by 5% and search for bigger faces in the image, repeating this process until it reaches a final size.
# smaller values mean higher accuracy, whilst larger values are faster...but are less accurate.
# minNeighbors -- tells python how many neighbors to search around the window. 5 is a good start point. feel free to experiment however.
#faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.05, minNeighbors=5)     # for easy picture
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)     # for hard picture
# detectMultiScale(image[, scaleFactor[, minNeighbors[, flags[, minSize[, maxSize]]]]]) -> objects
# detectMultiScale2(image[, scaleFactor[, minNeighbors[, flags[, minSize[, maxSize]]]]]) -> objects, numDetections
# detectMultiScale3(image[, scaleFactor[, minNeighbors[, flags[, minSize[, maxSize[, outputRejectLevels]]]]]]) -> objects, rejectLevels, levelWeights

for x,y,w,h in faces:
    #rectangle(image, start-coordinates, end-coordinates, color-in-BGR-format, line-thickness-for-rectangle)
    img=cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 3)

#print(type(faces))
print(faces)
# the 4 values resulting from detectMultiscale are the X value, Y value for starting location of the face and then the next 2 values are the height and width from that start pixel location

# remember in img.shape, that the first value is the height, then width.
resized = cv2.resize(img, (int(img.shape[1]/3), int(img.shape[0]/3))) # this threw a small cant convert float to int error, but thats only b/c its an infinite repeating dec. so the code can still handle the error no problem.

#cv2.imshow("Gray", gray_image)
cv2.imshow("Rectangle-drawn", img)
cv2.waitKey(3000)
cv2.destroyAllWindows()