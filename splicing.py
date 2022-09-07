a = [1,2,3,4,5,6,7,8]
b = ['q','r','s','t','u','v','w','x']

subA = []
subB = []

#splicing two lists together (not tuples here) in coorelation to the crossover function for genetic algorithms
c = None

subA = a[0:3]
subB = b[3:]
print(subA)
print(subB)

c = subA
print (c)

c.extend(subB)
print (c)


#testing out two-point crossover and one day k-point crossover
subA = a[3:7]   #pick the two crossover points, and take the associated segment and save it
subB = b[3:7]

d = a[:4]       #take the beginning of the chromosome, up to where the above begins its cutoff. Dont forget for splicing [start:stop] start includes the indicie you refer to, while stop excludes that number. TL;DR start is >= while stop is <
e = b[:4]
print(d)
print(e)

d[3:7] = e
print(d)

d.extend(a[7:])
print(d)

# just checking if splicing can handle a 'stop' of 0 ie [:0] and it can.
q = [5,10,15,20]
r = q[:0]
print ("r of [:0]: ", r)

r = q[0:0]
print ("r of [0:0]: ", r)

r = q[(len(q)-1):(len(q)-1)]
print ("r of [max-1:max-1]: ", r)

r = q[2:5]
print ("r of [max-1:max-1]: ", r)