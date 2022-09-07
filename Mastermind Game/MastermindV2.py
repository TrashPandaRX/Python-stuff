import csv
import sys # this is where im pulling exit() from
import numpy as np
import random
import HandlerV1_1

# this version of Mastermind is really trying to intergrate the Handler.py as the game progresses.

'''
So let see what this game technically needs (not in order):

Stretch goals:
*) (1/2) it would be interesting to set the # of tries and the length of the unknown code sequence
*) () try to implement a visual interface for the code in a web browser via DJANGO eventually
*) () try to implement a visual interface for the code as a popup window on the computer

Core goals:
a) (+) randomly generate a code sequence, as well as accept hardcoded codes for testing purposes
b) (+) evaluate if a code sequence is correct and port the results to the same CSV file:
    1) (+) return the # of pegs that are wrong position & wrong value
    XXX 2) (-) return the # of pegs that are right position & wrong value XXX SCRATCH THIS section, its totally useless
    3) (+) return the # of pegs that are wrong position & right value
    4) (+) return the # of pegs that are right position & right value
c) () accept user input, BUT add it to a separate file in CSV format
d) () read input in from CSV file
    1) () one line for the secret code
    2) () one line for the user's input
    3) () X # of lines for old guesses, and the evaluation result for that series of guesses
    4) () ?? I feel like im forgetting some important aspect
*) () EVENTUALLY design an AIs to solve the problem in a satisfactory manner.
    1) () planning algorithm
    2) () some sort of basic AI from my intro class
    3) () one day build an unsupervised machine learning alg
    4) () SCRATCH THIS --> build a supervised learning alg

*) be a fucking adult and put all the major groups of functions in separate files

*) make a version that allows duplicate values and one that disallows duplicates eg [1,1,6,3] vs [3,5,2,4]
'''

# testing to make sure import of Handler.py works
#fromCSV = Handler.readIn("readsample2.csv")


GameOver = False

maxInput = 4
numericalRange = 9  # the largest value for a peg usable, with the smallest being 1
totalTries = 8
currentTry = 1
historyInputs = [[-1 for i in range(maxInput)]for x in range(totalTries)]     # priorAttempts = [[-1]*maxInput for x in range(totalTries)] # same thing as history, just written different
# use list comprehensions! the innermost list comp fills the list with -1's for each numerical value,
# and the outer list comp establishes the total number of lists you will have as guesses
# tl;dr inner gives [-1,-1,-1,-1], and outer gives [[a], [b], [c], [d], ...]
# print (history) # just checking if list comp is correct
historyResults = [[-1]*3 for x in range(totalTries)]


lastInput = []  # last code user attempted
confirmed = []  # how many full misses, correct peg type/wrong loc, full correct were in the last submitted user code

userInput = []

_secretCode = [-1,-1,-1,-1] # what all user codes inputs will be compared against, if this is set to [-1,-1,-1,-1] randomly make a secret code, otherwise use given

# MAJOR: at present this implementation allows duplicate "peg types"
# 2/22/22 i added the temp portion to get rid of duplicate values for the code
def genCode(numericalRange:int, secretCode: list):
    if secretCode == _secretCode:
        newCode = secretCode
        for i in range(len(secretCode)):    # needed the number of elements in the list and for it to be treated as an iterable so i combined len() & range()
            temp = random.randint(1,numericalRange)
            while temp in newCode:
                temp = random.randint(1,numericalRange)
            newCode[i] = temp
        
        # be sure to cut this print() out in the future
        print(newCode)
        return newCode
    else:
        return secretCode

secretCode = genCode(numericalRange, _secretCode)


# vvvvvvvvvvv HANDLERV1_1 TESTING PART 1 vvvvvvvvvvv
#good spot for breakpoints
settings = [maxInput, numericalRange, totalTries, currentTry, secretCode]
handlerSettingTest = HandlerV1_1.importSettings(settings)
handlerRecallTest = HandlerV1_1.modifyData('game.csv')

print(handlerRecallTest)
# ^^^^^^^^^^   END OF TESTING PART 1   ^^^^^^^^^^^^^


# MAJOR: evaluate user input against secret code
# ps using trailing underscore after input because this naming convetion is used to avoid conflicts with Python keywords
# need to take in the user input as a string --> conv to list of string elements --> turn those string snippets into ints
def input_(attempt : str):
    try:
        # helps jump to the except block by combining if() & raise
        if (len(attempt) != maxInput):
            raise ValueError
        toList = list(attempt)
        intList = []

        for a in toList:
            # if the current int is outside the permitted range, raise a ValueError
            if ((1 <= int(a) <= numericalRange) == False):
                raise ValueError
            intList.append(int(a))

        print(intList)
        return (intList)

    except (TypeError, ValueError):
        # if you forget how to pass in variables, check "delftstack.com/howto/python/python-print-variable"
        print("you must input a series of {} integers from 1 to {}".format(maxInput, numericalRange))

def compare_(attempt : list, secret: list):
    '''
    b) () evaluate if a code sequence is correct and port the results to the same CSV file:
        1) () return the # of pegs that are wrong position & wrong value
        2) () return the # of pegs that are wrong position & right value
        3) () return the # of pegs that are right position & right value
    '''
    # respectively 100% wrong, wrong spot but right value, and right spot + right value
    wrong = 0
    # wrongList =[-1]*maxInput
    half = 0
    # halfList =[-1]*maxInput
    right = 0
    # rightList =[-1]*maxInput


    if (attempt == secret):
        print("YAY, YOU GUESSED IT!!!")
        right = 4
        # i hate having to use this global keyword. to modify "global" variables
        global GameOver
        GameOver = True

    else:
        # FIXED this portion of code is looking exclusively for wrongs and rights, no halves
        # Works finally -- 2/23/22 forgot to increment count
        count = 0

        for x in attempt:
            if x in secret:
                half += 1
            else:
                wrong += 1

            if secret[count] == x:
                half -=1
                right +=1
            count += 1

    print ("{} wrongs, {} half corrects, {} completely corrects".format(wrong, half, right))
    return [wrong, half, right]                    


# MAJOR: save old inputs and increment the current try count
def record(toSave : list, index : int, results: list):
    print (toSave)
    historyInputs[index] = toSave
    historyResults[index] = results

    # IMPORTANT, CURRENT, FIXME
    # this part ought to be written to the .csv file
    # atm i need to either access the submit() function within modifyData() or just make submit part of the overall modifyData() func...
    # or 3rd option i never considered... make submit() just a regular function and just add the file name to the required parameters
    temp = toSave
    temp.extend(results)
    HandlerV1_1.submit('game.csv', temp)



def view():
    count = 0
    for x in historyInputs:
        print ("Series {}: {} resulting in {}".format(count, historyInputs[count], historyResults[count]))
        count += 1
    print()



# actual "game loop"
while ((currentTry <= totalTries) and (GameOver == False)):
    print("attempt # {} of {}".format(currentTry, totalTries))
    attempt = input_(input())

    tempCode = attempt
    tempResults = compare_(attempt, _secretCode)
    record(tempCode, currentTry-1, tempResults)

    '''
    # works as intended, okay you can put this inside of record()
    test = attempt
    test.extend(tempResults)
    print("trying to make sure i can unify the attempt and results cleanly: ", test)
    '''


    view()

    # vvvvvvvvvvv HANDLERV1_1 TESTING PART 2 vvvvvvvvvvv
    #HandlerV1_1.modifyData('game.csv').submit()
    # ^^^^^^^^^^   END OF TESTING PART 2   ^^^^^^^^^^^^^

    currentTry += 1


#view()

sys.exit()

#attempt = input_("4613")
#compare_(attempt, _secretCode)