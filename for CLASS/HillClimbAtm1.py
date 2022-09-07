import matplotlib.pyplot as plt
from random import randint

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
	nCount = 0				# counter for which neigbhor indicie you are on.
	total = len(current)
	vNeighbor = []			# the highest value neighbor ( determined by valueFinder() ), must be passed out
	potentialNbrs = []			# single bit modified lists, based on current
	potentialNbrsResults = []	# integer values yielded from valueFinder() from each potential neighbor list
	onesInNbrs = 0			# holds total # of 1's in array to help construct x-axis for the plot portion


	for nCount in range(total):
		potentialNbrs.append(current)

		'''
		Example of what is basically happening below: @10:37pm 9/4
		
		INITIAL STATE
		potentialNbrs[][]
		
		0 - 1,0,1,0,1
		1 - 1,0,1,0,1
		2 - 1,0,1,0,1
		3 - 1,0,1,0,1
		4 - 1,0,1,0,1


		FLIP BIT STAGE (flip bit equal to what what nCount (the counter) currently is)
		nCount = 0, so
		-> 0 - [1],0,1,0,1		FLIP the BIT at potentialNbrs[0][0]		AFTERMATH 0 - [0],0,1,0,1

		END STATE
		potentialNbrs[][] after looping

		0 - 0,0,1,0,1
		1 - 1,1,1,0,1
		2 - 1,0,0,0,1
		3 - 1,0,1,1,1
		4 - 1,0,1,0,0

		'''
		if (potentialNbrs[nCount][nCount] == 0):	# [current indicie of the vCurrent copy passed in] [specific bit that needs to be FLIPPED]
			potentialNbrs[nCount][nCount] = 1
		
		else:				# maybe use elif instead of else:
			potentialNbrs[nCount][nCount] = 0

		nCount = nCount+1


	vFinderCount = 0		# counter to iterate through the loop below
	#neighborBool = False	# did we find the  neighbor value that yielded the highest value after being put in valueFinder()? -- 11:14pm 9/4 this might possibly be obsolete with how i handled the algorithm
	neighborAns = 0
	i = 0 					# "i" will be the int that holds the indicie the max() value is found at
	
	#while (vFinderCount < total || neighborBool != True):		# loop breaks when vFinderCount exceeds bounds of total (ie the number of total bits in the binary list) OR neighborBool becomes TRUE
	for vFinderCount in range(total):							# @10:11pm 9/4 hmm might actually want to remove this -- RESULTS:  NO INSTEAD we removed this from being under while()
		potentialNbrsResults.append(valueFinder(potentialNbrs[vFinderCount]))		# take value of current neighbor and put it in new list

			
	# @7:45pm 9/3 - trying to now determine which number out of all in potentialNbrsResults is the biggest -- SOLVED, use max()
	neighborAns = max(potentialNbrsResults)
	i = potentialNbrsResults.index(neighborAns)

	print(i)

	#10:04pm 9/4 need to determine the indicie of the neighbor thats been determined to yield the biggest value
	vNeighbor = potentialNbrsResults[i]

	#11:54am 9/5 added this to count the number of 1's in the chosen neighbor again so it can be returned at the end of the function
	#onesInNbrs = oneCounter(list(potentialNbrsResults[i]))	# @12:28pm 9/5 put potentialNbrsResults[i] inside of list(), @12:32pm 9/5 decided to try cutting 'onesInNmbrs' & 'vNbrAnsOnes' from code

	#neighborBool = TRUE 	# 11:14pm 9/4 this might possibly be obsolete with how i handled the algorithm

	#the lines under "while()" til "neighborBool = TRUE" were all a part of the while() loop until 11:14pm



	#I think i solved most of the issues with the above code using index() and vNeighbor[]

	#YOU CAN RETURN MULTIPLE VALUES IN PYTHON!!!
	return neighborAns, vNeighbor #, onesInNbrs


#---------------------------------------------------------------------	
#primary code flow
for t in range(MAX):

	local = False

	# declare variable to hold current v
	vCurrent = []
	vNeighbor = []
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

	# print(vCurResult) removed because i just needed to make sure oneCounter() & valueFinder() worked


	while (local != True):

		# select 40 new strings based on vCurrent
		# 1) create a loop that flips a bit, saves it to an array ***i made a whole function to do all of this stuff
		vNbrReturns = NGAMF(vCurrent)
		vNbrAnsValue = vNbrReturns[0]
		vNbrAnsBits = vNbrReturns[1]
		#vNbrAnsOnes = vNbrReturns[2]


		if (vCurAns < vNbrAnsValue):		# vNbrAns is the result of the chosen vNeighbor after going through valueFinder()
			print(vNbrAnsBits)
			vCurrent = list(vNbrAnsBits)	# if vNeighbor is BIGGER than vCurrent, vNeighbor becomes vCurrent

			# @11:49am 9/5 added for safetys sake
			clear(vNbrReturns)
			clear(vNbrAnsBits)

		else:
			local = True

			# final attempt to ensure that I didnt muck anything up earlier with vCurrent and vNeighbor values:
			# make it RECALCULATE the number of 1's in vCurrent (to be the x-axis) and the result of the function ( valueFinder() ) for the y-axis 
			vCF_X = oneCounter(vCurrent)
			vCF_Y = vCurAns


	plt.plot(vCF_X, vCF_Y, "ro")

	# TODO
	# Need to export the biggest value of each REPEAT to an external file named Output.txt

	t = t+1


plt.xlabel('# of ones')
plt.ylabel('greatest value')

plt.title('Hill Climber Algorithm')

plt.show()











