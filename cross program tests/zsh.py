import os
import subprocess
'''
zsh terminal ideas to test out~

1) while loop until a process succeeds
2)
3)
4)
5)
6)

'''
# failed
'''
bashTest = str(subprocess.check_output(['for x in 1 2 3; do echo $x; done']))
print(bashTest)
'''

# works
os.system('for x in 1 2 3; do echo $x; done')

username = "FRVNET1"
passTest = ["daniel","babygirl","11prV1091rqT","meeses"]

#os.system('networksetup -setairportnetwork en0 {} "{}"'.format(ssid, current_pass))
'''
for i in passTest:
'''    

#os.system('for x in daniel babygirl 11prV1091rqT meeses; do while networksetup -setairportnetwork en0 {}  [$? -ne 0] do true; done done'.format(username))
#os.system('for x in daniel babygirl moosical turbobash; do echo $x; done') # works
os.system('for x in daniel babygirl moosical turbobash; do while echo -n "Trying touch command $x..." touch $x [ $? -ne 0 ] do true ; done done')

cmd = 'for x in daniel babygirl moosical turbobash; do while echo -n "Trying touch command $x..." touch $x [ $? -ne 0 ] do true ; done done'

execute = subprocess.Popen(cmd, shell=True)

print(execute)
'''
for x in daniel babygirl 11prV1091rqT meeses; do
    while
        networksetup -setairportnetwork en0 {} "{}" [$? -ne 0]
    do true;
    done
done

'''