import matplotlib.pyplot as plt
from random import randint
import random

# 9/9/20 @~8:49am  IT WORKS! just clean up my comments and psychotic babble that I always have TRYING to explain my thought process

#----------------------------------------------------------------	
# Setup portion of Simulated Annealing
t = 0
MAX = 200
temp = 100		# testing 100 first, then 150, then 200

size = 0

# declare variable to hold current v
vCurrent = []		# list of 50 bits representing the current v
vNeighbor = []		# list of 50 bits representing the v found to have the largest value out of all 50 potential neighbors

potNeighbors = []	# contains all lists of potential neighbors to the current vCurrent
potFnNeighbors = []	# this contains the various valueFinder() numbers  got from potNeighbors

# holds the result of valueFinder(), aka the function, upon vCurrent & vNeighbor respectively
fCurrent = 0
fNeighbor = 0 

# for graph
vCF_Y = 0			# result of valueFinder() based on bits
lastBestVal = 0		# records whatever vCF_Y's prior greatest value was

#---------------------------------------------------------------------
# Functions:
def oneCounter(countMyOnes):
	r = 0
	for x in range (len(countMyOnes)):
		if countMyOnes[x] == 1:
			r = r+1

		# if current element is not 1, simply move to next iteration
		# nothing

	# return r value containing however many 1's you counted.
	return r

# performs f = |14 * oneCounter(bits of vCurrent) - 190| function
def valueFinder(vBits):
	return abs(14 * oneCounter(vBits) - 190)

def energyChange(fNeighbor, fCurrent):	# to be used where it says exp{} in the lecture documents
	return fNeighbor-fCurrent

def outputData(fileName, value, action):
	outputFile = open(f"{fileName}.txt", f"{action}")
	outputFile.write(f"{value}")
	outputFile.close()

#---------------------------------------------------------------------
# Simulated Annealing algorithm

# beginning of the output data for assignment for clarity's sake
outputData("Output", "Data from my Simulated Annealing Algorithm\n", "a")


#----------------------------------------------------------------	
# select a possible string of 50 bits at random -- FINE
x = 0

while (x < 50):
	vCurrent.append(randint(0,1))
	x = x+1

size = len(vCurrent)
#----------------------------------------------------------------	

# evaluate vCurrent using valueFinder(vCurrent's list of bits)
fCurrent = valueFinder(vCurrent)

# REPEAT -- (until stop-criteron)
while (temp > 0):

	k = 5 	# In my version/interpretation of this Algorithm,
				# (with the current temp settings, and other stuff)
				# THIS IS BY FAR THE MOST IMPORTANT VARIABLE
				# k ~ 5-10 ? you COULD hit a local maximum if you are unlucky with your seedElif value vCurrent
				# k ~ 15 ? graphs in decent detail, what is going on incrementally
				# k ~ 25 ? you will likely find the global maximum eventually
				# k ~ 50 ? you will ALMOST certainly find the global maximum (due to the sheer number of TERMINATION-CONDITION loops that will weed out local maxima and abuse the temperature cooling the most)
	

	# REPEAT -- (until termination-condition)
	while(k > 0):		# k is a standin value to control the "TERMINATION-CONDITION loop"

		#----------------------------------------------------------------------------
		# *** FORMERLY the function "NGAMF(vCurrent):" *** -- FINE
		# nearly identical code from HillClimb.py modified names of variables and also proof read for possible conflicts
		
		potNeighbors = [0] * size						# single bit modified lists, based on current
		potFnNeighbors = [0] * size						# integer values yielded from valueFinder() from each potential neighbor list

		for l in range(size):
			potNeighbors[l] = vCurrent[:]				# copy list of bits from vCurrent into pot[ential]Neighbors

			if (potNeighbors[l][l] == 0):				# [current indicie of the vCurrent copy passed in] [specific bit that needs to be FLIPPED]
				potNeighbors[l][l] = 1
			
			else:
				potNeighbors[l][l] = 0
		
		for h in range(size):
			potFnNeighbors[h] = valueFinder(potNeighbors[h])		# take value of current neighbor under scrutiny and put it in new list

		#------------------------Still part of NGAMF, but questionable-------------------
		i = randint(0,size) - 1

		vNeighbor = potNeighbors[i]			# to keep value in bounds according to the size of the bit-list
		fNeighbor = valueFinder(vNeighbor)
		#-------------------------------------------------------------------------------
		seedElif = random.random()			# this will be the value used for comparison in the elif branch just below

		# THEORETICALLY OKAY
		if (fCurrent < fNeighbor):			# if fCurrent is smaller than fNeighbor replace fCurrent with it
			vCurrent = vNeighbor[:]			# copy the bits of vNeighbor over vCurrent, ie vCurrent <-- vNeighbor
			fCurrent = fNeighbor 			# also replaces the fCurrent value with the fNeighbor value

		elif (seedElif < ( energyChange(fNeighbor, fCurrent)/temp ) ):
			vCurrent = vNeighbor[:]
			fCurrent = fNeighbor

		print(f"current STOP-CRITERION temp:{temp}-degrees,\ncurrent TERMINATION-CONDITION loop's greatest value: {fCurrent}")
		k = k-1
		# ^ TERMINATION-CONDITION ^
		
	#-------------------------------------------------------------------------------------
	
	vCF_Y = fCurrent

	# graph with different "dots" according to value
	if(vCF_Y == lastBestVal):
		plt.plot(t, vCF_Y, "g^")
	elif (vCF_Y < 350):
		plt.plot(t, vCF_Y, "bo")
	elif (351 < vCF_Y < 500):
		plt.plot(t, vCF_Y, "yo")
	elif (501 < vCF_Y < 1000):
		plt.plot(t, vCF_Y, "ro")

	# output greatest value (vCF_Y) to Output.txt
	if (t == 199):
		outputData("Output", f"{vCF_Y}.\n\n", "a")
	else:
		outputData("Output", f"{vCF_Y}, ", "a")

	lastBestVal = vCF_Y 					# to check to see if the last "best value" is the same as the current one, for the purposes of graph

	temp = temp - 0.5						# FINE
	t = t+1

	MAX = MAX - 1

	# print(f"current STOP-CONDITION: {MAX}\ncurrent temp: {temp}")
	# ^ STOP-CRITERION ^

# graph details
plt.xlabel('Current loop #')
plt.ylabel('greatest value from each "REPEAT"')

plt.title('Simulated Annealing Algorithm')

plt.show()

# END
