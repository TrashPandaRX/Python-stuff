import csv
from random import randint

'''
Structure of CSV file as i imagine it:

line 1) settings:
    col 1) length of secret code
    col 2) total # of guesses
    col 3) current guess out of total
    col 4)
line 2) the actual code
line 3) user's input/guess

Prior Guesses
*** maybe simplify the "# pegs" part to just correct peg type & correct peg type + correct peg location 
Fields: guess # | submitted code | # pegs WP & WV | # pegs RP & WV | # pegs WP & RV | # pegs RP & RV |
line 4)
line 5)
line 6)
line 7)
line 8)
etc


'''

codeLength = 4      # num of elements in the code sequence [a,b,c,d]
possibleValues = 6  # max numerical value usable within the code from 1, eg if 9 then codes COULD look like 3,3,4,9 or if 4 you COULDNT have 5,5,7,6
totalGuesses = 8
guessNum = 1

setCode = [None] * codeLength

def codeGenerator(valRange: int, cdLen: int):
    for i in range(cdLen):
        setCode[i] = randint(1,valRange)

codeGenerator(possibleValues, codeLength)

currentGuess = [None]*codeLength

def makeNew():
    default = [
        [codeLength, totalGuesses, guessNum],
        [setCode],
        [currentGuess]
    ]

    with open('game.csv', 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerows(default)

    def terminate():
        file.close()

# test case -- as of 2/15/22 it successfully builds the csv file (it does overwrite the formerly named one however, but to rectify that just tell it to rename the file to be +1 whatever the conflicting file's name is)
#makeNew()

#------------------------------------------------------
# read in .csv file data for mastermind game
# this part will be the tedious one, as i must ensure that lengths of code and values dont violate the parameters set by the first line or so of the .csv file

'''
# too many issues and shitty coding on my end. redo it
def readIn(fileName: str):
    with open(fileName, 'r') as file:
        reader = file.readlines()
        #return reader


        #temporarily passed over due to "return"
        fileContent = []
        for line in reader:
            #print(reader)  -- just regular print without formatting returns [] and \n character all over the place
            #print(line)    -- works okay, but it adds an extra line between each (prolly due to the \n character its handling from being read in)
            s = ''.join(line)

            fileContent.append("{}".format(s.strip()))   # bingo~ this passes in the {} arguments from the format()'s list of parameters. tl;dr {}{}{} = format.(a,b,c)

            t = "{}".format(s.strip())         # you can specify what gets stripped in the () otherwise it just strips whitespace

            u = list(t)
            print(u)

        return fileContent   # remember return ends the function, but yield permits it to continue

    def contents():
        return file
    
    def terminate():
        file.close()
'''

#try 2 of readIn()
# fiddling is going okay as of 11:13pm 2/18
def readIn(fileName: str):
    def cleaner(row : str):
        print(row)

        #remove junk like commas and \n
        #no need for the above when you use csv.reader()!
        try:
            a = []
            for each in row:
                a.append(int(each))
            print(a)
        except:
            alt = []
            for each in row:
                alt.append(each)
            print(alt)
        

    with open(fileName, 'r') as file:
        reader = csv.reader(file)   # this csv.reader() is optimized for reading in CSV files! dont forget it dummy, "reader = file.readlines()" is for reading it in as strings
        

        fileContent = []

        for line in reader:
            cleaner(line)

#readIn("readsample.csv")