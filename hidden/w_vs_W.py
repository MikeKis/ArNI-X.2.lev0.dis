# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 21:53:22 2024

@author: User
"""

import matplotlib.pyplot as plt
import numpy as np

wmin = -1
wmax = 3

# Data for plotting
W = np.arange(-10.0, 40.0, 0.1)
w = [wmin + (wmax - wmin) * max(WW, 0) / (wmax - wmin  + max(WW, 0)) for WW in W]

fig, ax = plt.subplots()
ax.plot(W, w)

ax.set(xlabel='W', ylabel='w',
       title='Dependence of the synaptic weight w on the synaptic resource W')
ax.grid()

plt.show()