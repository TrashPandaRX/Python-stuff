import cv2, time
from datetime import datetime
import pandas as pd
from numpy import genfromtxt

video = cv2.VideoCapture(0)

first_frame = None
status_list = [None,None]    #[None,None]
times = []
#df = pd.DataFrame(columns=["Start", "End"])     # this is a data frame dummy -- the way i was going to use this, following the tutorial was deprecated
df_initializer = pd.DataFrame(columns=["Start", "End"])
df_start_list = []
df_end_list = []


a = 0

#time.sleep(3)   # this little pause helps the delta feed be better and highlighting the differences between first_frame and the current frame, but it also makes the object detection via the threshold suck buttcheeks

# TODO i want to make it so that if pixels from first_frame match the current frame's pixels greyscale values to like a 85-90% accuracy within ~5-10 pixels location, ignore those pixels for
# the purposes of writing the threshold_frame. that is to say, if current pixels match the original pixel value, ignore it and set it to 0. but if its different, treat that as
# a contour and throw a rectangle around that instead. 

while True:
    a = a+1
    check, frame = video.read()

    status = 0 # denotes motion is not being detected in the current frame

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)   # we want to blur the image because it smooths the image and increases accuracy

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 140, 255, cv2.THRESH_BINARY)[1] # i usually use 140 during decent lighting
    # thresh_frame = cv2.threshold(delta_frame, 120, 255, cv2.THRESH_BINARY)[1] # this looks really cool when you also turn gaussianblur off
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # now we need to utilize find contours & draw contours
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        # modified by me
        if cv2.contourArea(contour) > 150000 or cv2.contourArea(contour) < 3000: # < 20000 or cv2.contourArea(contour) > 150000:
            continue
        '''
        # original
        if cv2.contourArea(contour) < 1000:
            continue
        '''
        status = 1
        (x,y,w,h) = cv2.boundingRect(contour)   # creating a rectangle if contour's area is greater than 1000 units
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3) # see face-detection-intro.py (yes, this is modifying 'frame')
    
    # ME: make this suck less
    # status_list.append(status) # original
    # my version to get rid of the None in status_list, this SHOULD replace those pesky None that the instructor had as placeholders in status_list
    if status_list[0] is None:
        status_list[0] = status
    elif status_list[1] is None:
        status_list[1] = status
    else:
        status_list.append(status)

    # if the last item in the list is 1 and the second to last item was 0 (ie 0 -> 1)
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
        print(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
        print(datetime.now())

 
    cv2.imshow("Video Feed", gray)
    cv2.imshow("Delta Frames", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Colored image w/ Rect", frame)

    key = cv2.waitKey(1)

    # added this myself
    if a == 50:
        print(gray)
        import numpy as np
        my_sample = cv2.imwrite(filename= 'frame_from_motion_detect_2.jpg', img= gray)
        my_sample = np.savetxt(fname = 'frame_from_motion_detect_2.csv', X = gray, delimiter = ',')   # just so you know the resulting csv file's total columns per row is every pixel in the width, 1280(width)x720(height)

    if key== ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

print(status_list)
#print(times)

for i in range(0,len(times), 2): #iterating through "times" variable, but taking 2 steps at a time because the start time is immediately followed by an end time. we want to leave those values paired up
    # https://stackoverflow.com/questions/70837397/good-alternative-to-pandas-append-method-now-that-it-is-being-deprecated
    #df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index = True) -- old, soon to be deprecated method using DataFrame.append()

    df_start_list.append(times[i])
    df_end_list.append(times[i+1])

print("Checking start values\n", df_start_list)
print("Checking end values:\n", df_end_list)

df_result = pd.DataFrame(columns = ["Start", "End"])
print("CLOSEUP A:\n", df_result)
#df_result = pd.concat([df_result, pd.Series(data = df_start_list, name = "Start"), pd.Series(data = df_end_list, name = "End")], ignore_index = True)   # not what i wanted and im making things WAY harder than it needs to be

df_result["Start"] = df_start_list
df_result["End"] = df_end_list
print("CLOSEUP B:\n", df_result)


#df.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows
