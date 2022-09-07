# https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_quick_guide.htm
import random
from random import randint

'''
CREATED 11:00am on 12/17/21
UPDATED @ 2:57pm on 12/19/21

# IT WORKS!!! ofc it can be improved upon

Genetic Algorithm:

population initialization
			V
loop (until termination criterion reached):
	fitness function calculation			# another interesting idea for the fitness test...maybe make it change every few generations to simulate a changing/evolving environment
			V
	Crossover of chromosomes
			V
	Mutation
			V
	Survivor Selection

Terminate and return best solutions





Fitness Function:
takes solutions as input and evaluates how good of a solution it is to the problem




Since im just starting out ill do the classic GA where you use binary chromosomes.

chromosomes will consist of 16 genes whose alleles could be either 1 or 0

'''
#---------------------------------------------------------------------
# VARIABLES:

#these are the variables to modify if you want to expand the duration of generational breeding or increase the complexity of the chromosomes.
build_chromosomes = 2500
chromoLength = 20
totalGenerations = 15

curChromo = []
parentChrmA = []
parentChrmB = []
# assessedAlready = {}	# this is a set! ie unordered, unchangable, but doesnt permit DUPLICATE VALUES, EDIT: placed within the executable portion of code

#determined via fitness()
lowFitness = [] # less than 0
avgFitness = []	# between 0 and 21
highFitness = [] # greater than 21

#determined by passing in low,avg,and high fitness lists to parentSelection
#these variables hold who has been chosen to help yield the next generation,
#and who will NOT pass on their genes.
makeKids = []
noKids = []

mutationPoints = []

iCC = []	# initial chromosome collection
currentCollection = []
survivingCollection = []
parentCollection = []
eliminatedCollection = []

#finalCollection = {}


#---------------------------------------------------------------------
# FUNCTIONS:

def chromosomeBuilder(length):
	chromosome = list(range(length))
	gene = 0

	a = 0 	# a is the counter for what gene of the chromosome you are picking

	'''
	while (a < length):
		gene = randint(0,1)
		a += 1
	'''

	# for each item in the list 'chromosome', choose that indicie's value aka that gene's allele as either 0 or 1.
	for x in chromosome:
		gene = randint(0,1)
		# print (gene)
		chromosome[x] = gene

	return chromosome



def chooseCrossPoint(chromoLength, onepoint):
	crosspointA = None
	crosspointB = None
	if (onepoint == True):
		#crosspointA cannot be 0 or the max of the chromosome length, so the permissible ranges are from 1...max-1
		crosspointA = randint(1,chromoLength-2)	# -2 instead of -1 because chromoLength would just be the last indidice of the list, whereas -2 lets you choose the indicie before the last

		return crosspointA, crosspointB

	#two-point or k-point crossovers
	else:
		crosspointA = randint(1,chromoLength-2)
		crosspointB = randint(0,chromoLength-1)

		# just in case crosspointB is the same value as crosspointA, keep rerolling the value until its different
		if (crosspointA == crosspointB):
			while (crosspointA == crosspointB):
				crosspointB = randint(0,chromoLength-1)

		return crosspointA, crosspointB


# replaced the parameters crossoverA and crossoverB with the points[] to be less dependant upon parameters being passed in
# parentA & parentB should be "chromosomes" ie lists, and crossoverA & crossoverB should be integers
# def crossover(parentA: list, parentB: list, crossoverA: int, crossoverB: int):
# a better alternative:
def crossover(parentA: list, parentB: list, onepoint: bool):
	parentAseg1 = []
	parentAseg2 = []
	parentAseg3 = []
	parentBseg1 = []
	parentBseg2 = []
	parentBseg3 = []

	unionA = None
	unionB = None

	# only doing one point crossover
	if(onepoint is True):
		print("entered a crossover with onepoint being true")
		# setup the parameters for the method that will choose the crossover points
		points = chooseCrossPoint(len(parentA) , onepoint)

		print ("Crossover point for this is: ", points[0]) 
		print(" and if this is multipoint crossover, then the other point is ", points[1])

		#create two substrings at the crossover point
		parentAseg1 = parentA[0:points[0]]
		parentAseg2 = parentA[points[0]: len(parentA)]

		parentBseg1 = parentB[0:points[0]]
		parentBseg2 = parentB[points[0]: len(parentB)]

		#just a quick check
		print(parentAseg1, " checking pAs1, before .extend()")
		print(parentAseg2, " checking pAs2, before .extend()")
		print(parentBseg1, " checking pBs1, before .extend()")
		print(parentBseg2, " checking pBs2, before .extend()")


		#cross the first segment of parentA with the second segment of parentB, and then 1st seg of parentB with 2nd seg of parentA
		# noticed @ 7:19pm 12/19/21
		# hmm it appears after some more tinkering, that using the assignment operator linked the memory address of unionA to that of parent_seg_
		# meaning that this .extend() operation is affecting both the union variable as well as the original parent_seg_ variable
		
		#tests
		'''
		parentAseg1.extend(parentBseg2)
		unionA = parentAseg1
		parentBseg1.extend(parentAseg2)
		unionB = parentBseg1

		VS

		unionA = parentAseg1.extend(parentBseg2)
		unionB = parentBseg1.extend(parentAseg2)

		# i found an explaination! https://stackoverflow.com/questions/40511075/why-does-this-function-return-different-results
		# apparently .extend() and .append() apply list modifications IN-PLACE which means that the changes happen instantly
		# and so due to this property unions in the second test are still None as oppose to the first test where they dont have to compete
		# with an in-place operation that seizes control of that line of code instead of performing the extend/append and then putting
		# the result of that into union_
		'''

		#original (that works fine, just made me a little confused on why union was acting weird. I discovered the issue tho)
		unionA = parentAseg1
		unionA.extend(parentBseg2)
		unionB = parentBseg1
		unionB.extend(parentAseg2)

		#just a quick check
		#print(parentAseg1, " checking pAs1, after .extend()")
		#print(parentAseg2, " checking pAs2, after .extend()")
		#print(parentBseg1, " checking pBs1, after .extend()")
		#print(parentBseg2, " checking pBs2, after .extend()")

		print(unionA, " unionA within crossover w/ onepoint = True")
		print(unionB, " unionB within crossover w/ onepoint = True")

		return unionA, unionB

	#two point or k-point crossover
	elif (onepoint == False):
		print("entered a crossover with onepoint being false, ie multiple crossover points")

		points = chooseCrossPoint(len(parentA) , onepoint)

		#segment each parent chromosome into three parts
		parentAseg1 = parentA[0:points[0]]			#start
		parentAseg2 = parentA[points[0]:points[1]]	#middle
		parentAseg3 = parentA[points[1]:len(parentA)] #end
		parentBseg1 = parentB[0:points[0]]			#start
		parentBseg2 = parentB[points[0]:points[1]]	#middle
		parentBseg3 = parentB[points[1]:len(parentB)] #end

		#now restructure the two chromosomes
		unionA = parentAseg1
		unionA.extend(parentBseg2)
		unionA.extend(parentAseg3)
		unionB = parentBseg1
		unionB.extend(parentAseg2)
		unionB.extend(parentBseg3)

		print(unionA, " unionA within crossover w/ onepoint = False")
		print(unionB, " unionB within crossover w/ onepoint = False")	

		return unionA, unionB

	else:
		print("something went wrong in the crossover portion, or an incompatible parameter was used")



def parentSelection(low: list, avg: list, high: list):
	#40% chance low fit reproduce, 60% chance avg fit reproduce, 100% high fit reproduce
	
	# handle lowfitness chromosomes first
	# epp stands for 'each potential parent'
	for epp in low:
		odds = randint(0,99) 		# 0 to 100
		if (odds > 59): 			# 40% chance of becoming parent
			makeKids.append(epp)	# add current chromosome to 'makeKids' list
			lowFitness.remove(epp)	# and remove it from the list of lowFitness potential parents
		else:
			noKids.append(epp)
			lowFitness.remove(epp)

	# then avgfitness
	for epp in avg:
		odds = randint(0, 99)
		if (odds > 39):				# 60% chance of becoming parent
			makeKids.append(epp)
			avgFitness.remove(epp)
		else:
			noKids.append(epp)
			avgFitness.remove(epp)

	# lastly highfitness
	for epp in high:
		odds = randint(0,99)
		if (odds >= 0):				# 100% chance
			makeKids.append(epp)
			highFitness.remove(epp)
		else:
			noKids.append(epp)
			highFitness.remove(epp)

	# if theres an odd # of parents just accept one of the rejects
	# FIXME THIS WAS THE CAUSE OF MY ISSUES!!! Its pulling out a list and shoving it into the indicie of another list, producing this fuckery "example: [[0,0,0,0,0,0,1,1]]"
	# i replaced .append() with .extend() and it fixed it!
	if (len(makeKids)%2 == 1):
		makeKids.extend(random.sample(noKids, 1))

	#might need to return the lists to the caller, idk yet havent even had a chance to test the code out


# you'll need to modify this if you want to account for more than a binary genes
def mutation(chromosome):
	mutate = randint(0,999)

	#edit this percentage if i want to make it more likely to test this function
	#originally set to 5, changed to 999 for testing purposes
	if (mutate <= 5):
		chosenGene = randint(0,chromoLength-1)
		#newAllele = randint(0, whateverAllelesUsed)
		print(chosenGene, " chosenGene")
		print(chromosome, " chromosome")
		print(chromosome[chosenGene], " chosenGene within chromosome")


		newAllele = chromosome[chosenGene]
		print("newAllele = ", newAllele)

		if (chromosome[chosenGene] == 0):
			print("chosen gene's allele will go from 0->1")
			newAllele = 1
		elif (chromosome[chosenGene] == 1):
			newAllele = 0
			print("chosen gene's allele will go from 1->0")


		chromosome[chosenGene] = newAllele
		print (chromosome, " this chromosome should have successfully been mutated.")

		return chromosome

	else:
		print (chromosome, " this chromosome did not mutate.")
		return chromosome




def survivorSelection(population):
	survivors = []
	deaths = []

	for each in population:
		fitCalculated = fitness(each)
		die = randint(0,99)


		#for highFitness
		if (fitCalculated >= round((chromoLength*3)/3, 1)):
			if (die <= 1):	# 2% chance to die
				#add to failures
				deaths.append(each) 
			else:
				survivors.append(each)

		#for avgFitness
		elif (round((chromoLength*1)/3, 1) < fitCalculated <= round((chromoLength*3)/3, 1)):
			if (die <= 9):	# 10% chance to die
				#add to failures
				deaths.append(each) 
			else:
				survivors.append(each)

		#for lowFitness
		else:
			if (die <= 29):	# 30% chance to die
				#add to failures
				deaths.append(each) 
			else:
				survivors.append(each)

		#for lowFitness
	return survivors
'''
def initializePop():
'''

def oneCounter(countMyOnes):	# from SimulatedAnnelingtry3
	r = 0
	for x in range (len(countMyOnes)):
		if countMyOnes[x] == 1:
			r = r+1

		# if current element is not 1, simply move to next iteration
		# nothing

	# return r value containing however many 1's you counted.
	return r

# from SimulatedAnnelingtry3, modified numbers a bit.
def fitness(chromosome):
	#return abs(7 * oneCounter(chromosome) - 21)
	return oneCounter(chromosome)


def determineResults(population):
	for each in population:
		if (fitness(each) > 5):	# got lazy here, i hardcoded the minimum fitness value id accept
			print (each)

#---------------------------------------------------------------------
curChromo = chromosomeBuilder(chromoLength)

print(curChromo, "tester generation")

# POPULATION INITIALIZATION
# randomly generates a list of chromosomes with a predetermined chromosome length, and also quantity of chromosomes
for x in range (build_chromosomes):
	iCC.append(chromosomeBuilder(chromoLength))
	print(iCC[x])

# LOOP'S TERMINATION CONDITION
# can do a few things depending on how i want to do this...
# 1) x number of generations passed 2) have x number of high quality solutions
# 3) population dips below a certain size

chromosomeCollection = iCC

#FITNESS CALCULATION
currentGen = 0
while (currentGen < totalGenerations):			# conundrum, should I use a set of prefixed crossover points for a whole generation or make it on a chromosome by chromosome basis?
	print("+++++++++++++++++++++ CURRENT GENERATION: ", currentGen, " +++++++++++++++++++++")
	#select crossover points ahead of time  -- Scratch that

	#ideally i should one day develop a means to determine fitness within a percentile system.
	#like how dumb people might score in between the 1st to like 49th percentile, average people might be 50th to like 80th, and genuis would be 81st up to 99th percentile.
	# http://www.behavioradvisor.com/701Percentiles.html

	#might need to tighten these values up down the line
	for r in chromosomeCollection:
		fitCalculated = fitness(r)
		if 	(fitCalculated <= round((chromoLength*1)/3, 1)):
			lowFitness.append(r)
		elif (round((chromoLength*1)/3, 1) < fitCalculated <= round((chromoLength*2)/3, 1)):
			avgFitness.append(r)
		elif (fitCalculated >= round((chromoLength*3)/3, 1)):
			highFitness.append(r)

	'''
	print("low fitness:", lowFitness)
	print("---------------")
	print("average fitness", avgFitness)
	print("---------------")
	print("high fitness", highFitness)
	'''

	#PARENT SELECTION
	parentSelection(lowFitness, avgFitness, highFitness)

	'''
	#CROSSOVER -- not working i fucked up the list mid loop so this is no good.
	while (len(makeKids) > 0):
		i = randint(0, len(makeKids))	# pick random parent from those who were chosen to make kids
		
		
		#dont repick chromosomes
		#while (i == assessedAlready):
		#	i = randint(0, len(makeKids))
		

		parentChrmA = makeKids[i]
		currentCollection.append(makeKids[i])
		assessedAlready.append(i)

		i = randint(0, len(makeKids))
		parentChrmB = makeKids[i]
		currentCollection.append(makeKids[i])
		assessedAlready.append(i)

		theChildren = crossover(parentChrmA, parentChrmB, True)	# chromosomome, chromosome, onepoint crossover or not? T/F	

		#MUTATION
		theChildren = mutation(theChildren)

		# add the child to the population
		currentCollection.append(theChildren)
	'''


	#CROSSOVER v2.0
	count = 0
	total = len(makeKids)/2
	print (len(makeKids), "length of makeKids")

	print("make kids segment start #######################")
	for o in makeKids:
		print(o)
	print("make kids segment end #######################")

	assessedAlready = []
	while(count < total):

		# **** ISSUE ****
		# Ive tracked down the issue with the parents being splcied wrong to around here at least @11:10am.
		# for some reason some of the parents are being put inside of lists when they are already lists, and it fucks everything else up beyond this point.
		# Example: @ crossover, count: 8 ------- current pair:  [[0, 1, 0, 0, 1, 0, 1, 0]] [0, 0, 1, 1, 0, 0, 1, 0]

		print("@ crossover, count:", count)
		pair = random.sample(makeKids,2)
		print("current pair: ", pair[0], pair[1])
		assessedAlready.append(pair[0])
		#print("successfully added parent 1 to assessedAlready")
		assessedAlready.append(pair[1])
		#print("successfully added parent 1 to assessedAlready")

		makeKids.remove(pair[0])
		makeKids.remove(pair[1])


		# ****I GOOFED @10:37am, 12/17/21 i neglected the fact that crossover produces TWO children not from the parents ****

		theChildren = crossover(pair[0], pair[1], True)
		print(theChildren, " --> theChildren, there are no technical issues if this value ISN'T  'None'")

		#MUTATION
		Child1PostMutation = mutation(theChildren[0])
		Child2PostMutation = mutation(theChildren[1]) 

		print(Child1PostMutation, " Child1PostMutation regardless if actually mutated or not")
		print(Child2PostMutation, " Child2PostMutation regardless if actually mutated or not")


		# add the parents and child to the population
		currentCollection.append(Child1PostMutation)
		currentCollection.append(Child2PostMutation)
		currentCollection.append(pair[0])
		currentCollection.append(pair[1])

		count += 1
		print ("------------------------------------------")

	print("sucessfully left crossover, and right before survivorSelection")

	#SURVIVOR SELECTION
	#add the chromosomes back to the pop who didn't breed
	currentCollection.extend(noKids)

	currentCollection = survivorSelection(currentCollection)


	#Iterate generation
	currentGen += 1

#finalCollection = set(currentCollection)
finalCollection = currentCollection

#RESULTS
#return a set (unique chromosomes only) of the most fit results
for finalists in finalCollection:
	rating = fitness(finalists)
	if (rating > int(chromoLength*.7)):
		print("Most fit children: ", finalists, " & fitness rating: ", rating)


