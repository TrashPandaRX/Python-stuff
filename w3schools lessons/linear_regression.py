import matplotlib.pyplot as plt
from scipy import stats

# model that is a decent fit for linear regression model

x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

slope, intercept, r, p, std_err = stats.linregress(x, y)

# https://www.w3schools.com/python/python_ml_linear_regression.asp
# the x is the independent variable, and return is the y (dependent var)
# y = mx+b in other words, return (slope*x)+intercept
def myfunc(x):
  return slope * x + intercept

# map() is a really useful way to execute a function multiple times with a list of different inputs
mymodel = list(map(myfunc, x))
print(mymodel)
print(r, " : r-value is the relationship value (or lack thereof between x-axis values and y-axis values). -1 to 1 indicate a 100%\ correlation, where a 0 means no relationship. Pearson correlation coefficent. r squared is the coefficent of determination")
print(p, " : p-value for a hypothesis test whose null hypothesis is that the slope is zero,\n using Wald Test with t-distribution of the test statistic.\n aka P-Value is a statistical test that determines the probability of extreme results\n of the statistical hypothesis test, taking the Null Hypothesis to be correct.\n It is mostly used as an alternative to rejection points that provides the smallest level of significance\n at which the Null-Hypothesis would be rejected.")
'''
HOW DO I INTERPRET THE P-VALUES IN LINEAR REGRESSION ANALYSIS?
The p-value for each term tests the null hypothesis that the coefficient is equal to zero (no effect). A low p-value (< 0.05) indicates that you can reject the null hypothesis. In other words, a predictor that has a low p-value is likely to be a meaningful addition to your model because changes in the predictor's value are related to changes in the response variable.

Conversely, a larger (insignificant) p-value suggests that changes in the predictor are not associated with changes in the response.
'''
plt.scatter(x, y)
plt.plot(x, mymodel, ':og')
plt.show()

# model that is a BAD fit for linear regression model
x = [89,43,36,36,95,10,66,34,38,20,26,29,48,64,6,5,36,66,72,40]
y = [21,46,3,35,67,95,53,72,58,10,26,34,90,33,38,20,56,2,47,15]

slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))
print(r, "-- r value, ", p, "-- p value")

plt.scatter(x, y)
plt.plot(x, mymodel, ':^y')
plt.show()


