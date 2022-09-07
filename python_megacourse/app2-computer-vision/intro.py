import cv2
import numpy as np
import os   # needed because cv2.imread() is picky with directory paths

# ------------------- Fiddling around with code ---------------------
'''
# WORKS
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "galaxy.jpg")
img = cv2.imread(file_path, 1)

# changed from int to float (seems to work so far) YAY! specifiying the dtype = np.uint8 permitted imwrite & imshow (more the latter than the former) to function properly!
mini = np.arange(start = 0.0, stop = 255.0, dtype= np.uint8)
updated = mini.reshape((15,17))

print(mini)
print(updated)

cv2.imwrite('0to254.jpg', updated)
cv2.imshow("greyscale", updated)
cv2.waitKey(0)
'''

'''
# Old broken version:
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "galaxy.jpg")
img = cv2.imread(file_path, 1)

mini = np.arange(0, 255)
updated = mini.reshape((15,17))

print(mini)
print(updated)

cv2.imwrite('0to254.jpg', updated)
cv2.imshow("greyscale", updated)
cv2.waitKey(0)
'''
#------------------ end of fiddling w/ code --------------------------

# ------------------ Modifying lecture code somewhat ----------------
# inner .abspath(__file__) gets the directory of the script being run.
# middle part's .dirname() returns the directory of the file_name passed in as an argument OR the parent directory of the last indicated item in the path which could in practice be another directory
# and the outermost .join() adds the .jpg name to the existing path
#file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "galaxy.jpg")

# imread(image_name, -1 : transparency capabilities (color w/ transparency) / 0: Greyscale / 1: BGR (aka color image) ...OR cv2.COLOR_BGR2RGB does what it implies) DO NOTE...opencv uses BGR as default, while matplotlib yses RGB...
#img = cv2.imread(file_path, 0)
#img = cv2.imread(file_path, 1)
#img = cv2.imread(file_path, cv2.COLOR_BGR2RGB)
#img = cv2.imread(file_path, 1)

#print(file_path)
# print("\n",os.path.abspath(__file__))
#print(type(img), "\n", img)
# you can also get the dimensions of the file indirectly through numpy via the ndarray.shape property
#print(img.shape)
#print(img.ndim) # lets you see how many dimensions of the file you are working with, should be 2 here as an image is 2D. i wonder if 3d models would yield .ndim of three ...hmmm

#cv2.imshow("Galaxy", img)
#cv2.waitKey(0) # if you put 0 for this, it will close the window when any button input is detected

#mini = np.arange(0, 255)
#updated = mini.reshape((15,17))

#print(mini)
#print(updated)

#cv2.imwrite('0to254.jpg', updated)
#cv2.imshow("greyscale", updated)
#cv2.waitKey(0)
#generated_img = cv2.
#------------- (EOF) Modifying lecture code somewhat (EOF) ----------------

# ------------- Lecture code ---------------
# inner .abspath(__file__) gets the directory of the script being run.
# middle part's .dirname() returns the directory of the file_name passed in as an argument OR the parent directory of the last indicated item in the path which could in practice be another directory
# and the outermost .join() adds the .jpg name to the existing path
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "galaxy.jpg")

img = cv2.imread(file_path, 0)

print(type(img))
print(img)
print(img.shape)
print(img.ndim)

resized_image = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2))) # new dimensions should be passed in as a tuple (width, height)

cv2.imshow("Galaxy", resized_image)
cv2.waitKey(4000) # this is in milliseconds, so 2000 would be 2 seconds. if you put 0 it stays indefinitely till a keyboard button is pressed
cv2.destroyAllWindows()

cv2.imwrite("galaxy_grey.jpg", img)