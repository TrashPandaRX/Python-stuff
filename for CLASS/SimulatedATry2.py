import matplotlib.pyplot as plt
from random import randint
import random

# 9/8/20 @~10:06 pm

#----------------------------------------------------------------	
# Setup portion of Simulated Annealing
t = 0			# also known as tCounter for the purposes of tempCoolant()
MAX = 200

'''
MAX = 200 used to be here (above), until i realized this could act as k-times
the inner loop could run, otherwise you would look to see if
termination-condition's chck to see if 'thermal equilibrium' has been
reached ie whether the probability distribution of the selected new
strings approaches the boltzmann distribution.

MAX has since been moved to the beginning of the for loop @9/7 ~4pm


'''
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
vCF_X = 0		# of bits for current valueFinder()
vCF_Y = 0		# result of valueFinder() based on bits
vCF_Z = 0		# temperature

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

#---------------------------------------------------------------------
# Simulated Annealing algorithm
#for q in range(MAX):

#----------------------------------------------------------------	
# select a possible string of 50 bits at random
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

	k = 50
	# REPEAT -- (until termination-condition)
	while(k > 0):		# k is a standin value to control the "TERMINATION-CONDITION loop"

		#------------------------------------------------------------------------------------------------------------
		# *** FORMERLY the function "NGAMF(vCurrent):" ***
		# essentially this bit of code simply generates potential neighboring v values of vCurrent
		
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

			# print(f"potential neighbors' resulting value: {potFnNeighbors[h]}")	***

		i = randint(0,size) - 1

		print(f"the value from 0 to {size}, is {i}")

		vNeighbor = potNeighbors[i]	#to keep it in bounds

		#-------------------------------------------------------------------------------

		fNeighbor = valueFinder(vNeighbor)

		#print(f"the vNeighbor is:\n{vNeighbor}\n\nthe fNeighbor is:\n{fNeighbor}\n\nthe vCurrent is:\n{vCurrent}\n\nthe fCurrent is:\n{vNeighbor}\n")

		if (fCurrent < fNeighbor):
			vCurrent = vNeighbor[:]					# copy the bits of vNeighbor over vCurrent, ie vCurrent <-- vNeighbor
			fCurrent = fNeighbor

			# print(f"the vCurrent from the *if branch* is:\n{vCurrent}")			***
			# plt.plot(vCF_X, vCF_Y, "bo")											***

		elif (random.random() < ( energyChange(fNeighbor, fCurrent)/temp ) ):
			vCurrent = vNeighbor[:]
			fCurrent = fNeighbor

		k = k-1


			# print(f"the vCurrent is from the *elif branch* is:\n{vCurrent}")
			# plt.plot(vCF_X, vCF_Y, "bo")

		# in case neither the if nor the elif trigger, you the 	

		

		# print(f"current TERMINATION-CONDITION: {MAX}")							***
		# ^ TERMINATION-CONDITION ^
		
	#-------------------------------------------------------------------------------------
	
	vCF_X = oneCounter(vCurrent)
	vCF_Y = fCurrent
	vCF_Z = temp

	plt.plot(vCF_Y, vCF_Z, "bo")

	temp = temp - 0.5
	t = t+1

	MAX = MAX - 1

	print(f"current STOP-CONDITION: {MAX}\ncurrent temp: {temp}")
	# ^ STOP-CRITERION ^

# graph
plt.xlabel('function results')
plt.ylabel('temperature')

plt.title('Simulated Annealing Algorithm')

plt.show()
# END













