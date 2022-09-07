import matplotlib.pyplot as plt
import numpy as np
import math

#https://www.w3schools.com/python/matplotlib_pie_charts.asp

y = np.array([35, 25, 25, 15])
mylabels = ["Apples", "Bananas", "Cherries", "Dates"]

def convert_deg2rad(deg:float):
    print(deg)
    radian_ = float('{0:.3f}'.format(deg*(math.pi/180)))    # formula to convert a degree to radians and format it to only keep the first 3 dec places.
    print(type(radian_), radian_)

# 1 radian = (180*pi)° aka degrees
def convert_rad2deg(rad:float):
    degrees_ = rad*(180*math.pi)
    print(degrees_)
    return degrees_

convert_rad2deg(11)
plt.pie(y, labels = mylabels, startangle = convert_rad2deg(1))  # FIXME its still always somewhat off. im probably fucking something super obvious up... facepalm
plt.show()