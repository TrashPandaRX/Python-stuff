import numpy as np
import matplotlib.pyplot as plt

#https://www.w3schools.com/python/matplotlib_histograms.asp
x = np.random.normal(100, 1, 1000)

print(x)

plt.hist(x)
plt.show()