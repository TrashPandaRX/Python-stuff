import cv2, time

video = cv2.VideoCapture(0)

first_frame = None

a = 0.0

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
    thresh_frame = cv2.threshold(delta_frame, 100, 255, cv2.THRESH_BINARY)[1] # cv2.threshold() returns a tuple, and we need the second item in the tuple which is the frame data.
    # in order to smooth out those black holes in the "Threshold frame" window, we need to use cv2.dilate
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # now we need to utilize find contours & draw contours
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue

        (x,y,w,h) = cv2.boundingRect(contour)   # creating a rectangle if contour's area is greater than 1000 units
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3) # see face-detection-intro.py (yes, this is modifying 'frame')


    cv2.imshow("Video Feed", gray)
    cv2.imshow("Delta Frames", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Colored image w/ Rect", frame)


    key = cv2.waitKey(1)
    print(gray)

    if key == ord('q'):
        break

print(a)
video.release()
cv2.destroyAllWindows
