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
for i in 2 3 4 5 ; do
    # Retry logic
    while
        echo -n "Trying external_command $i... "
        # Call the external command
        external_command $i
        # $? is the return code, 0 if successful
        [ $? -ne 0 ]
    do true ; done
done