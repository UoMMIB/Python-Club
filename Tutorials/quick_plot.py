import matplotlib.pyplot as plt
import math

def f(x):
    return math.sin(x)


x = [i/100 for i in range(0,1000)]
y = list(map(f,x))

plt.plot(x,y, color='k', linestyle='--')
plt.show()
