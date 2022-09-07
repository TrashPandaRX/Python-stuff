import cv2, time

from numpy import genfromtxt

video = cv2.VideoCapture(0)

first_frame = None

a = 0.0

time.sleep(3)   # this little pause helps the delta feed be better and highlighting the differences between first_frame and the current frame

while True:
    a = a+1
    check, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)   # we want to blur the image because it smooths the image and increases accuracy

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)

    # no movement compared to original frame, make this black
    # else if there is movement, ie pixel value greater than 30 make the pixel white (255 in greyscale)
    thresh_frame = cv2.threshold(delta_frame, 160, 255, cv2.THRESH_BINARY)[1] # cv2.threshold() returns a tuple, and we need the second item in the tuple which is the frame data.
    # in order to smooth out those black holes in the "Threshold frame" window, we need to use cv2.dilate
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # now we need to utilize find contours & draw contours
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        # modified by me
        if cv2.contourArea(contour) < 30000 or cv2.contourArea(contour) > 120000:
            continue
        '''
        # original
        if cv2.contourArea(contour) < 1000:
            continue
        '''
        (x,y,w,h) = cv2.boundingRect(contour)   # creating a rectangle if contour's area is greater than 1000 units
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3) # see face-detection-intro.py (yes, this is modifying 'frame')


    cv2.imshow("Video Feed", gray)
    cv2.imshow("Delta Frames", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Colored image w/ Rect", frame)


    key = cv2.waitKey(1)

    # added this myself
    if a == 50:
        print(gray)
        import numpy as np
        my_sample = cv2.imwrite(filename= 'frame_from_motion_detect.jpg', img= gray)
        my_sample = np.savetxt(fname = 'frame_from_motion_detect.csv', X = gray, delimiter = ',')   # just so you know the resulting csv file's total columns per row is every pixel in the width, 1280(width)x720(height)

    if key== ord('q'):
        break

print(a)
video.release()
cv2.destroyAllWindows
