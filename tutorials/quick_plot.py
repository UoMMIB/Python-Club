import matplotlib.pyplot as plt
import math

'''
Plot sin(x)
'''
def f(x):
    # f(x) = sin(x)
    return math.sin(x)


x = [i/100 for i in range(0,1000)] # 0:10, step size:0.1
y = list(map(f,x)) # f(x)

plt.plot(x,y)
plt.show()
