#do varibles initialized outside a for loop get permenantly modified after the for loop ends?
#RESULT: YES IT DOES

'''
a = 0
b = 0

for a in range(10):
	b = b+1
print("iteration test:")
print(a)
print(b)

print("max() & index() tests:")

c = [123,12341,9843,330, 9914, 385, 17, 43986]

print(c.index(max(c), 0, len(c)))	#works fine, searches c[] for the biggest value among all indicies, and returns the indicie that contains the biggest value.
'''

j = []
j.append(0)
j.append(1)
j.append(0)
j.append(1)
j.append(0)
print(f"j list: {j}")

a = []
b = []
c = []
d = []
e = []
f = [a,b,c,d,e]

x = []
m = 0

for n in range(len(f)):
	f[n] = j
	
print(f"f collection:\n{f[0]},\n{f[1]},\n{f[2]},\n{f[3]},\n{f[4]}")

f[0][0] = 1
f[1][1] = 0
f[2][2] = 1
f[3][3] = 0
f[4][4] = 1

# LOOK HERE FOOL
# ***2:28pm 9/6 ...oh my fucking god IS IT FUCKING UP BECAUSE THE VALUE OF J WAS PASSED IN BY REFERENCE, AND SO MODIFYING F IN FACT MODIFIES J WHICH EVERY MOTHER FUCKING ELELEMT OF F IS TIED TO?!?
# ***if future me cant understand basically im saying that imagine theres a ball that is shared by 5 different dimensions. ANYTHING THAT HAPPENS TO THAT BALL IS REFLECTED IN EVERY DIMENSION'S. Like dimension 1 me draws an X on the ball. Then dimensions 2-5 have an X on their ball as well.

print(f"f modified:\n{f[0]},\n{f[1]},\n{f[2]},\n{f[3]},\n{f[4]}")
print (f"f modified:\n{f[0]},\n{f[1]},\n{f[2]},\n{f[3]},\n{f[4]}")

'''
for n in range(len(f)):
	print(f"f collection of loop:\n{f[0]},\n{f[1]},\n{f[2]},\n{f[3]},\n{f[4]}")
	if (f[n][n] == 0): 
		f[n][n] = 1
		print(f[n][n])
		print(f[n])
	else:
		f[n][n] = 0
		print(f[n][n])
		print(f[n])
'''


