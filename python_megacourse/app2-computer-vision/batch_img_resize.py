# Exercise for lesson no. 151
# need to pass in each image within the target directory
# read image in as cv2
# modify
# save modified images separately

# NOTE!!! .DS_Store fucks with this script if its found in the sample_images directory. delete that shit if its there

import os
import numpy as np
import cv2

def choose_dir(dir: str):        
    try:
        input_source = os.path.join(os.path.dirname(os.path.abspath(__file__)), dir)
        files_tuple = tuple(os.listdir(input_source))
        print("completed safely")
        return files_tuple, input_source
    except:
        print("crashed n burned bro within choose_dir()")

def alter_images(path2imgs : str, imgs_to_modify):
    newdir_path = os.path.join(path2imgs, "resized_versions")
    if os.path.exists(newdir_path):
        print(f"Before removal: designated dir exists? {os.path.exists(newdir_path)}\n{os.listdir(path2imgs)}")
        import shutil
        shutil.rmtree(newdir_path)
        print(f"After removal: designated dir exists? {os.path.exists(newdir_path)}\n{os.listdir(path2imgs)}")

    try:
        for current_image in imgs_to_modify:
            # passes through the loop:

            # BUG -- Status: FIXED
            # testing to see if this fixes the issue with imgs_to_modify
            # only consisting of files after the shutil.rmtree()
            # but after what should be the final pass, it somehow recognizes the newly created directory: '/resized_versions'
            # and tries to treat it as a file...which i do NOT want
            # WOO BREAK THROUGH AFTER 15 min! got it to work ~~~ Go me ~~~ (this was pretty simple, i did take a break to eat oatmeal which was why this took 15 whole min, ahaha)
            print("current item is a file? ", os.path.isfile(os.path.join(path2imgs, current_image)))
            if os.path.isdir(os.path.join(path2imgs, current_image)):
                continue
            print(current_image)
            cv2_img = cv2.imread(os.path.join(path2imgs, current_image), 1)
            resized = cv2.resize(cv2_img, (100,100))

            # just to show the resized version
            cv2.imshow(current_image, resized)
            cv2.waitKey(1500) # this is in milliseconds, so 2000 would be 2 seconds. if you put 0 it stays indefinitely till a keyboard button is pressed
            cv2.destroyAllWindows()

            if not os.path.exists(newdir_path):
                os.mkdir(newdir_path)

            cv2.imwrite(os.path.join(newdir_path, f"{str(resized.shape[1])}x{str(resized.shape[0])}__{current_image}"), resized) # imwrite((path-to-save-img : path, new-file-name : str), cv2-imgdata-to-use : cv2-Mat)
        print("Resizing script complete!")
    except:
        print("Something went wrong in alter_images()")
#input("Type the exact name of the directory within the CWD containing images to process: ")
dir_of_images = choose_dir('sample_images')
alter_images(dir_of_images[1], dir_of_images[0])