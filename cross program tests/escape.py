#import argparse # parsing to the command line
import os
import subprocess
import csv
from time import sleep

bashTest = ""

print("This is the current working directory: ", os.getcwd())
#os.system('touch gooboy')   # works perfectly
#print(dir(os))
#os.system('networksetup -listallhardwareports')

'''
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
#ssid = "Extell's iPhone XR"
#password = "xrpkzg3qzcchf"

#os.system('networksetup -setairportnetwork en0 "{}" {}'.format(ssid, password))
#os.system('networksetup -setairportnetwork en0 BNWiFi NONE')    # Works!

target = ""
unknown = ""

# https://www.delftstack.com/howto/python/python-open-file-in-different-directory/ when using 'pathlib.Path()' Dont use / instead use \
# Volumes/Education/CSCI/Prgm\ Langs/Python/advanced/cross\ program\ tests/crack_databases/rockyou.txt
database = "crack_databases/rockyou.txt"
data = set()
data2 = set()
dataLength = 0
lastPassword = ""


with open(database, 'rb') as file:
    try:
        for _ in file:
            temp = _[:-1]# gotta remove the stupid \n, apparently if you do -2 you remove the n and the last letter of the string. the escape character --> \ isnt counted in the str
            #print(temp)
            data.add(temp)
            dataLength += 1
            lastPassword = temp
    except:
        print("stopped at {}, with length: {}".format(lastPassword, dataLength))
        print("failed")

print(dataLength)
sleep(3)


for _ in data:
    temp = _.decode('latin1')
    #print(temp)
    data2.add(temp)

print(data2)




#os.system('networksetup -setairportnetwork en0 {} "{}"'.format(target, unknown))    # Works!


#os.system('moo1moo1gas')  # you can add the password response like this