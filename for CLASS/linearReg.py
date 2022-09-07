import matplotlib.pyplot as plt

'''Each of these has 15 x or y values, paired together they form 15 xy point pairs'''
xValues = [3, 41, 7, 1, 4, 9, 8, 5, 2, 13, 19, 8, 22, 4, 29]
yValues = [8, 11, 16, 3, 9, 9, 12, 6, 10, 24, 26, 17, 15, 25, 12]

plt.plot(xValues, yValues, 'bo')

n = len(xValues)	#get the length of the lists, it doesnt matter if i choose x or y as they BETTER be the same length

'''
if i was parsing in the list of values from an external document or as userinput

for loop
'''

sumX = 0
sumX2 = 0
sumY = 0
sumXY = 0

for i in range(n):
	sumX = sumX + xValues[i]
	sumX2 = sumX2 + xValues[i] * xValues[i]
	sumY = sumY + yValues[i]
	sumXY = sumXY + xValues[i] *yValues[i]

b = (n * sumXY - sumX* sumY) / (n * sumX2 - sumX * sumY)
a = (sumY - b * sumX) / n

#y = a + (b * x?) no idea how you determine x, ik its the INDEPENDENT variable while y is the DEPENDENT.

#plt.plot( (a +(b + x)) , 'r--')	#no clue if this is right, x prolly is the biggest offender
plt.plot( a , 'r^')
plt.plot( b , 'g^')

plt.xlabel('x - axis')
plt.ylabel('y - axis')

plt.title('Simple Linear Regression')

plt.show()
	