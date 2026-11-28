import numpy as np
import matplotlib.pyplot as plt
angels = [k*np.pi/180 for k in range(360)]  #0-359 to pi

x = [np.sin(3*a)  *np.cos(a) for a in angels]   ## r * cos
y = [np.sin(3*a)  *np.sin(a) for a in angels]   ## r * sin


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect(1)
ax.plot(x,y)