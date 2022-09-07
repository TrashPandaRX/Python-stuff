import matplotlib.pyplot as plt
from random import randint

# CREATED 9/6 @ ~8:30pm

#---------------------------------------------------------------------
# Variables
t = 0						# counts up to MAX
MAX = 100					# max number of repeats algo should run

#---------------------------------------------------------------------
#Functions:


# step through list, if theres a 1 at location, increment o++ otherwise move to next
def oneCounter(countMyOnes):
	# 1) establish a variable that will be your counter
	r = 0

	# 2) loop to each element in the array/list
	for x in range (len(countMyOnes)):

		# 2.a) if current element is a 1, increment the counter and proceed
		if countMyOnes[x] == 1:
			r = r+1

		# 2.b) if current element is not 1, simply move to next iteration
			# nothing

	# 3) return r value containing however many 1's you counted.
	return r


# performs f=|13 * oneCounter(vCurrent) - 170| function
def valueFinder(vBits):
	return abs(13 * oneCounter(vBits) - 170)

# creates a list of "neighbors" for the vCurrent bit-list
def NGAMF(current):			# neighbors Generator And Maximum Finder
	loopCounter = 0				# counter for which neigbhor indicie you are on.
	listSize = len(current)
	vNeighbor = []			# the highest value neighbor ( determined by valueFinder() ), must be passed out as a LIST
	
	potentialNbrs = [0] * len(current)			# single bit modified lists, based on current
	# potentialNbrs[0] = current[:] just testing to ensure that current's values were copied, not the fucking reference to the value. aka the "passing by object/object value"

	# print(f"Hopefully I sliced/copied the contents of 'current' properly:\n{potentialNbrs}") # yup							***

	potentialNbrsResults = [0] * len(current)	# integer values yielded from valueFinder() from each potential neighbor list
	#onesInNbrs = 0			# holds total # of 1's in array to help construct x-axis for the plot portion


	for loopCounter in range(listSize):
		potentialNbrs[loopCounter] = current[:]

		if (potentialNbrs[loopCounter][loopCounter] == 0):	# [current indicie of the vCurrent copy passed in] [specific bit that needs to be FLIPPED]
			potentialNbrs[loopCounter][loopCounter] = 1
		
		else:				# maybe use elif instead of else:
			potentialNbrs[loopCounter][loopCounter] = 0

		loopCounter = loopCounter+1

	# print(f"modified bits of potentialNbrs:\n{potentialNbrs}")																***

	vFinderCount = 0		# counter to iterate through the loop below
	#neighborBool = False	# did we find the  neighbor value that yielded the highest value after being put in valueFinder()? -- 11:14pm 9/4 this might possibly be obsolete with how i handled the algorithm
	neighborAns = 0
	i = 0 					# "i" will be the int that holds the indicie the max() value is found at
	
	#while (vFinderCount < listSize || neighborBool != True):		# loop breaks when vFinderCount exceeds bounds of listSize (ie the number of total bits in the binary list) OR neighborBool becomes TRUE
	for vFinderCount in range(listSize):							# @10:11pm 9/4 hmm might actually want to remove this -- RESULTS:  NO INSTEAD we removed this from being under while()
		potentialNbrsResults[vFinderCount] = valueFinder(potentialNbrs[vFinderCount])		# take value of current neighbor and put it in new list

	# print(f"valueFinder() of potentialNbrs:\n{potentialNbrsResults}")															***

			
	# @7:45pm 9/3 - trying to now determine which number out of all in potentialNbrsResults is the biggest -- SOLVED, use max()
	neighborAns = max(potentialNbrsResults)
	# print(f"contents of neighborAns IN THE NGAMF():\n{neighborAns}")															***


	i = potentialNbrsResults.index(neighborAns)

	# print(f"Location of the highest value bit sequence in the potentialNbrsResults:\n{i}")									***

	# ************ LEFT OFF HERE!!! ************

	#10:04pm 9/4 need to determine the indicie of the neighbor thats been determined to yield the biggest value
	vNeighbor = potentialNbrs[i]

	# print(f"contents of vNeighbor IN THE NGAMF():\n{vNeighbor}")																***


	#YOU CAN RETURN MULTIPLE VALUES IN PYTHON!!!
	return [neighborAns, vNeighbor]					# https://www.geeksforgeeks.org/g-fact-41-multiple-return-values-in-python/ explains the diff ways you can return the values

#---------------------------------------------------------------------	
#primary code flow
for t in range(MAX):

	local = False

	# declare variable to hold current v
	vCurrent = []
	vNeighbor = []

	tramumaReducer = 0

	#----------------------------------------------------------------	
	# randomize a string of 40 bits
	x = 0

	while x<40:
		vCurrent.append(randint(0,1))
		x = x+1

	#----------------------------------------------------------------

	# evaluate vCurrent, @11:47am 9/5 modified to fit NGAMF's 2 return values, edited 11:52am RETURNS 3 values now
	vCurAns = valueFinder(vCurrent)
	vNbrReturns = [] 	# contain both returns of NGAMF
	vNbrAnsValue = 0 	# NGAMF[0], the max value
	vNbrAnsBits = []	# NGAMF[1], the bit list
	#vNbrAnsOnes = 0		# total # of ones to make x-axis for plot

	vCF_X = 0 #Current Final v result from oneCounter(vCurrent)
	vCF_Y = 0 #Current Final v result from valueFinder(vCurrent)


	while (local != True):
		print(f"New loop #{tramumaReducer}")
		tramumaReducer += 1
		# select 40 new strings based on vCurrent
		# 1) create a loop that flips a bit, saves it to an array ***i made a whole function to do all of this stuff
		vNbrReturns = NGAMF(vCurrent)

		# print(f"contents of vNbrReturns[0], supposed to be the result of valueFinder() from NGAMF:\n{vNbrReturns[0]}")		***
		# print(f"contents of vNbrReturns[1], supposed to be a list:\n{vNbrReturns[1]}")										***



		vNbrAnsValue = vNbrReturns[0]
		vNbrAnsBits = vNbrReturns[1]

		#print(vNbrAnsValue)
		#print(vNbrAnsBits)


		#vNbrAnsOnes = vNbrReturns[2]

		print(f"Current value: {vCurAns} vs  Neighbor's Value: {vNbrAnsValue}")

		if (vCurAns < vNbrAnsValue):		# vNbrAns is the result of the chosen vNeighbor after going through valueFinder()
			# print(f"contents of vNbrAnsBits:\n{vNbrAnsBits}")																	***
			vCurrent = vNbrAnsBits[:]		# if vNeighbor is BIGGER than vCurrent, vNeighbor becomes vCurrent

			print(f"vCurrent: {vCurrent}")
			print(f"vNbrAnsBits: {vNbrAnsBits}")

			# @11:49am 9/5 added for safetys sake
			# vNbrReturns.clear()
			# vNbrAnsBits.clear()

		else:
			local = True

			# final attempt to ensure that I didnt muck anything up earlier with vCurrent and vNeighbor values:
			# make it RECALCULATE the number of 1's in vCurrent (to be the x-axis) and the result of the function ( valueFinder() ) for the y-axis 
			vCF_X = oneCounter(vCurrent)
			vCF_Y = vCurAns
		


	#plt.plot(vCF_X, vCF_Y, "ro")

	# TODO
	# Need to export the biggest value of each REPEAT to an external file named Output.txt

	tramumaReducer = tramumaReducer + 1
	print(f"Reduce thine anxiety: {tramumaReducer}")

	t = t+1


#plt.xlabel('# of ones')
#plt.ylabel('greatest value')

#plt.title('Hill Climber Algorithm')

#plt.show()











