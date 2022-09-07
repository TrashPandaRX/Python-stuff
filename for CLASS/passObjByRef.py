a = [0,1,2,3,4,5]
b = a

print (a)
print (b)

# test to see if modifying b really modifies a at the same time. -- RESULTS: YES, fk me. it does change both of them
b[2:3] = ['c','d']

print (a)
print (b)

# yep .clear() wipes both out... 
a.clear ()

print (a)
print (b)

# lets try this instead... SUCCESS! AND EVEN BETTER I FOUND Q&A on the web that explain how to create bigass lists and modify them without hitting the snags i had!
a = []
b = []
c = []
d = []
z = [a,b,c,d]

print(f"A list containing 4 other empty lists:\n{z}")

for x in range(len(z)):
	z[x] = [0,1,0,1,0]
	print(z[x])

print(f"a: {a}")
print(f"b: {b}")
print(f"c: {c}")
print(f"d: {d}")
print(f"z: {z}")

print(f"z[0]: {z[0]}")
print(f"z[1]: {z[1]}")
print(f"z[2]: {z[2]}")
print(f"z[3]: {z[3]}")

for x in range(len(z)):
	if (z[x][x] == 0):
		z[x][x] = 1
	else:
		z[x][x] = 0

print(f"flipped z bits:\n{z}")
