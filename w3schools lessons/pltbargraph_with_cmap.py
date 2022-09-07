#Three lines to make our compiler able to draw:
# used help from this stack overflow response to use cmap to add colors to bar graph: https://stackoverflow.com/questions/64068659/bar-chart-in-matplotlib-using-a-colormap
import sys
import matplotlib
# 'agg' is a nongui backend, so you cant show the figure with it enabled
#matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

x = np.array(["A", "B", "C", "D", "E"])
y = np.array([3, 8, 1, 10, 5])
colors = plt.get_cmap("viridis")

rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))

plt.bar(x, y, color=colors(rescale(y)))#, cmap='nipy_spectral')
plt.show()

#Two  lines to make our compiler able to draw:
#plt.savefig(sys.stdout.buffer)
#sys.stdout.flush()