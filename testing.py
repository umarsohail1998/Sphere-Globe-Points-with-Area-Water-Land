
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm
from matplotlib import animation
import matplotlib.colors as colors

# %matplotlib inline
fig = plt.figure(facecolor="Black")
ax = plt.axes(projection="3d")
u =  np.linspace(0, 2*np.pi, 100)
v =  np.linspace(0, np.pi, 100)
r = 10
x = r * np.outer(np.cos(u), np.sin(v))
y = r * np.outer(np.sin(u), np.sin(v))
z = r * np.outer(np.ones(np.size(u)), np.cos(v))

random_color = colors.rgb2hex(np.random.rand(3))
ax.set_facecolor(random_color)

def init():
    ax.plot_surface(x, y,z, rstride=100, cstride=50, cmap=cm.RdPu)
    return fig,

def animate(i):
    ax.view_init(elev=20, azim=i*4)
    return fig,

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=90, interval=200, blit=False )
plt.show()