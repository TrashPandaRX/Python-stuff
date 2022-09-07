import numpy
import matplotlib.pyplot as plt

ages = [5,31,43,48,50,41,7,11,15,39,80,82,32,2,8,6,25,36,27,61,31]

# https://www.w3schools.com/python/python_ml_percentile.asp
# Percentiles are used in statistics to give you a number that describes the value that a given percent of the values are lower than.
# What is the 75. percentile? The answer is 43, meaning that 75% of the people are 43 or younger.
x = numpy.percentile(ages, 99)

print(x)

#added this bit myself to see the histogram breakdown
plt.hist(ages,8)
plt.show()