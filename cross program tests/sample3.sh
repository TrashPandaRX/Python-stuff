#!/bin/zsh

# Simulate an external command that randomly fails
function external_command {
    if [ $[ $RANDOM % $1 ] -eq 0 ] ; then
        echo "succeed"
        return 0
    else
        echo "failed"
        return 1
    fi
}

# Iterate over your predefined tests
# "xrpkzg3qzcchf"
#networksetup -setairportnetwork en0 "Extell’s iPhone XR" "wrongpass"
networksetup -setairportnetwork en0 "FRVNET1" "11prV1091rqT"
echo $? # returns Error: -3912  The operation couldn’t be completed. (com.apple.wifi.apple80211API.error error -3912.)0
# what if i made python look for any output from the terminal that had Error in it, and forced it to continue