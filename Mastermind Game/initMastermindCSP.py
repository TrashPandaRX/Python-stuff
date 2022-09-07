from hashlib import new
import HandlerV1_1
import itertools

# Evaluate data from Handler eg game.csv first, base data for variables, data and constraints based off this
gameData = HandlerV1_1.modifyData('game.csv')

print(gameData)

# requires 2d array to access settings data
# DOMAIN: max number you can use for the input from 1-9 at max
domain = [_ for _ in range(gameData[0][1])]
print(domain)

# VARIABLES: needs the 'length of code' ie how many digits will go into the codes
variables = [gameData[0][0]]
print(variables)

'''
#   CONSTRAINT: rules that dictate what values 'variables' can be:
#   1. () needs to acknowledge that you cant have duplicate values within the code
#   2. () cant exceed the domain's greatest numerical value (or a smarter way of saying this is, dont exceed gameData[0][1])
#   3. () dont pick values acknowledged as completely wrong
#   4. () you have a limited # of guesses indicated by gameData[0][2] & gameData[0][3], gameData[0][3] < gameData[0][2] aka (current try < total tries)
'''
# constraint likely needs to be a function to encompass this degree of complexity me thinks
constraint = [gameData[0][2],gameData[0][3]] #this is def wrong, dont be attatched

# defaulting possible solutions to -1 * (length of code)
# this might actually need to be a list or maybe even a dictionary...perhaps even a set since we do want UNIQUE solutions
possSol = list([-1]*gameData[0][0])
print(possSol)

'''
def validSolutions(domain : list, potentials: list):
    for x in range(100):

    yield potentials

validSolutions(domain, possSol)
'''


# we need permutations with no repeated values,
# n! / (n-r)!
# where n is the number of things to choose from, and we choose r of them, no repetitions, and order matters
def permutations_(pool : int, toChoose : int, codeLen: int):
    poolList = [_+1 for _ in range(pool)]
    chooseList = [_+1 for _ in range(len(poolList)-toChoose)]   # ahaha...i goofed, this part is the (n-r) bit but instead of that i had (n*r)...oops

    #print(poolList, chooseList)

    tempA = 1                   #n!
    # tempB = len(poolList)     #n
    tempC = 1                   #(n-r)!
    result = 0
    for each in poolList:
        tempA = each*tempA
        #print(tempA)
    
    for each in chooseList:
        tempC = each*tempC
        #print(tempC)

    
    result = tempA/tempC
    result = int(result)
    print(result)

    #allPermutations = set()

    basedCodes = list(itertools.permutations(poolList, toChoose))       # python is so useful~~ they have a built in permutation generator itertools.permutations(listToIterate,limitedSizeOfResult = None)
    #allPermutations.add(basedCodes)

    print("there are: {} unique codes!\nHere they are: {}".format(len(basedCodes),basedCodes))

    return basedCodes

possibilites = permutations_(9,4,4)
remaining = possibilites.copy()
print("remaining:\n",remaining)
#remaining.copy(possibilites)

print("items in possibilities", len(possibilites))
skip = 1
count = len(possibilites)


for x in possibilites:
    print(x)
    if count == 0:
        break
    if x in remaining:
        for each in x:
            print(each)

            # wrong
            for y in possibilites:
                print(y)
                if each == y[0] and y in remaining:
                    remaining.remove(y)
    count = count -1
    #print("what's left:\n", remaining)  # after first pass the last for loop (involving y), eliminates all codes that begin with 1 2 3 and 4
    print("cycling...")

print(remaining)




'''
abbreviations: WV - wrong value (eg 100% wrong), WP - wrong position (good value, needs repositioning), GJ - right value and right position in the code

Grading thresholds:

    () if code results in all WV, dispose of all the values from that attempt from the domain.
    () if the code results in WV & WP, try to test each value 

'''