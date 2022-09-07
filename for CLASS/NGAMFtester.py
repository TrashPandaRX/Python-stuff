from random import randint

# @1:26pm 9/5/20 currently trying to find out why despite incrementation working fine, the "append(valueFinder())"" part not only copies the same value across the entire list,
# but also doesn't even take the HIGHEST VALUE

# Variables
t = 0						# counts up to MAX
MAX = 100					# max number of repeats algo should run

#---------------------------------------------------------------------
#Functions:

# *** WORKS ***
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


# *** WORKS ***
def valueFinder(vBits):
	return abs(13 * oneCounter(vBits) - 170)

# *** ??? ***
def NGAMF(current):			# neighbors Generator And Maximum Finder
	nCount = 0				# counter for which neigbhor indicie you are on.
	total = len(current)

	print(f"total length of current: {total}")

	vNeighbor = []			# the highest value neighbor ( determined by valueFinder() ), must be passed out
	potentialNbrs = []			# single bit modified lists, based on current
	transitionSet = []		# ****NEW as of 12pm 9/6, maybe use an intermediary list instead of trying to work entirely on one list?
	potentialNbrsResults = []	# integer values yielded from valueFinder() from each potential neighbor list
	onesInNbrs = 0			# holds total # of 1's in array to help construct x-axis for the plot portion


	for nCount in range(total):
		potentialNbrs.append(current)

	print(f" initializing all rows to the current, ie {potentialNbrs}")
	print(f" tried valuefinder() on potentialNbrs: {valueFinder(potentialNbrs)}")

	nCount = 0	# before doing this, nCount = 39
	oCount = 0

	#what did i DO to cause the bits that I flipped in earlier iterations to all be set to the current set of flipped bits
	for nCount in range(total):
		for oCount in range(total):

			if (potentialNbrs[nCount][oCount] == 0):	# [current indicie of the vCurrent copy passed in] [specific bit that needs to be FLIPPED]
				print(f"potential neighbors, before flip: {potentialNbrs[nCount][oCount]}")
				potentialNbrs[nCount][oCount] = 1
				print(f"potential neighbors, flipped 0 to 1: {potentialNbrs[nCount][oCount]}")
			
			else:				# maybe use elif instead of else:
				print(f"potential neighbors, before flip: {potentialNbrs[nCount][oCount]}")
				potentialNbrs[nCount][oCount] = 0
				print(f"potential neighbors, flipped 1 to 0: {potentialNbrs[nCount][oCount]}")

		print(f"passed neighbor into valueFinder: {valueFinder(potentialNbrs[oCount])}\n")


	print(f"Potential Neighbors post bit flipping: {potentialNbrs}")


	vFinderCount = 0		# counter to iterate through the loop below
	#neighborBool = False	# did we find the  neighbor value that yielded the highest value after being put in valueFinder()? -- 11:14pm 9/4 this might possibly be obsolete with how i handled the algorithm
	neighborAns = 0
	i = 0 					# "i" will be the int that holds the indicie the max() value is found at
	
	#while (vFinderCount < total || neighborBool != True):		# loop breaks when vFinderCount exceeds bounds of total (ie the number of total bits in the binary list) OR neighborBool becomes TRUE
	for vFinderCount in range(total):							# @10:11pm 9/4 hmm might actually want to remove this -- RESULTS:  NO INSTEAD we removed this from being under while()
		print(f"vFinderCount currently: {vFinderCount}")
		potentialNbrsResults.append(valueFinder(potentialNbrs[vFinderCount]))		# take value of current neighbor and put it in new list

	print(f"**vFinderCount after loop: {vFinderCount}")
	# @7:45pm 9/3 - trying to now determine which number out of all in potentialNbrsResults is the biggest -- SOLVED, use max()
	neighborAns = max(potentialNbrsResults)


	print(f"neighborAns: {neighborAns}")

	i = potentialNbrsResults.index(neighborAns, potentialNbrsResults[0], len(potentialNbrsResults))

	print(f"the indicie containing the biggest value is: {i}")

	vNeighbor = potentialNbrsResults[i]

	return neighborAns, vNeighbor



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

	vNbrReturns = NGAMF(vCurrent)

	print(vNbrReturns)