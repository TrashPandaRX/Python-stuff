import matplotlib.pyplot as plt
from random import randint

# CREATED 9/6 @ ~8:30pm
# TODO	--	9/8 MOSTLY done need to double check comments and ALSO *** ADD IN THE CODE THAT PRINTS RESULTS TO 'Output.txt' ***

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
#---------------------------------------------------------------------
# Special Function -- Output to file

def outputData(fileName, value, action):	# "name of tile to output to", "what you want to output to the file", "r/w/a"
	outputFile = open(f"{fileName}.txt", f"{action}")
	outputFile.write(f"{value}")
	outputFile.close()

#---------------------------------------------------------------------	
#primary code flow

outputData("Output", "Data from my Hill-Climb Algorithm\n", "a")

for t in range(MAX):

	local = False

	# declare variable to hold current v
	vCurrent = []		# list of 40 bits representing the current v
	vNeighbor = []		# list of 40 bits representing the v found to have the largest value out of all 40 potential neighbors

	#----------------------------------------------------------------	
	# randomize a string of 40 bits
	x = 0

	while x<40:
		vCurrent.append(randint(0,1))
		x = x+1

	#----------------------------------------------------------------

	# evaluate vCurrent, @11:47am 9/5 modified to fit NGAMF's 2 return values, edited 11:52am RETURNS 3 values now
	vCurAns = valueFinder(vCurrent)
	listSize = len(vCurrent)
	vNbrReturns = [] 	# contain both returns of NGAMF
	neighborAns = 0 	# NGAMF[0], the max value
	vNeighbor = []	# NGAMF[1], the bit list
	#vNbrAnsOnes = 0		# total # of ones to make x-axis for plot

	vCF_X = 0 #Current Final v result from oneCounter(vCurrent)
	vCF_Y = 0 #Current Final v result from valueFinder(vCurrent)


	while (local != True):
		
		# select 40 new strings based on vCurrent
		# 1) create a loop that flips a bit, saves it to an array ***i made a whole function to do all of this stuff

		#------------------------------------------------------------------------------------------------------------
		# *** FORMERLY NGAMF(current): ***
		
		potentialNbrs = [0] * listSize			# single bit modified lists, based on current
		potentialNbrsResults = [0] * listSize	# integer values yielded from valueFinder() from each potential neighbor list

		for loopCounter in range(listSize):
			potentialNbrs[loopCounter] = vCurrent[:]

			if (potentialNbrs[loopCounter][loopCounter] == 0):	# [current indicie of the vCurrent copy passed in] [specific bit that needs to be FLIPPED]
				potentialNbrs[loopCounter][loopCounter] = 1
			
			else:				# maybe use elif instead of else:
				potentialNbrs[loopCounter][loopCounter] = 0

		
		for h in range(listSize):							# @10:11pm 9/4 hmm might actually want to remove this -- RESULTS:  NO INSTEAD we removed this from being under while()
			potentialNbrsResults[h] = valueFinder(potentialNbrs[h])		# take value of current neighbor and put it in new list

		neighborAns = max(potentialNbrsResults)

		i = potentialNbrsResults.index(neighborAns)
		vNeighbor = potentialNbrs[i]
		#------------------------------------------------------------------------------------------------------------

		vCurAns = valueFinder(vCurrent)


		print(f"Current value: {vCurAns} vs  Neighbor's Value: {neighborAns}")

		if (vCurAns < neighborAns):		# vNbrAns is the result of the chosen vNeighbor after going through valueFinder()
			# print(f"contents of vNeighbor:\n{vNeighbor}")																	***
			vCurrent = vNeighbor[:]		# if vNeighbor is BIGGER than vCurrent, vNeighbor becomes vCurrent

			print(f"vCurrent: {vCurrent}")
			print(f"vNeighbor: {vNeighbor}")

			plt.plot(oneCounter(vCurrent), vCurAns, "go")

		else:
			local = True

			# final attempt to ensure that I didnt muck anything up earlier with vCurrent and vNeighbor values:
			# make it RECALCULATE the number of 1's in vCurrent (to be the x-axis) and the result of the function ( valueFinder() ) for the y-axis 
			vCF_X = oneCounter(vCurrent)
			vCF_Y = vCurAns
	

	# output greatest value (vCF_Y) to Output.txt
	if (t == 99):
		outputData("Output", f"{vCF_Y}.\n\n", "a")
	else:
		outputData("Output", f"{vCF_Y}, ", "a")


	plt.plot(vCF_X, vCF_Y, "ro")

	# TODO
	# Need to export the biggest value of each REPEAT to an external file named Output.txt

	t += 1
	print(f"# of times Hill-Climb has been repeated {t}")


plt.xlabel('# of ones')
plt.ylabel('greatest value')

plt.title('Hill Climber Algorithm')

plt.show()


