# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 00:08:49 2023

@author: User
"""

import matplotlib.pyplot as plt
import numpy as np
import random

FramePresentationTime = 10
totnFrames = 3000
maxFrequency = 0.3
outfile = "../Workplace/clusters.txt"
labelfile = "../Workplace/cluster_labels.txt"

a = np.ndarray((3, 31, 31))
for x in range(31):
    for y in range(31):
        a[0, y, x] = np.exp(((x - 15) * (x - 15) + (y - 15) * (y - 15)) / -100)
for x in range(31):
    for y in range(31):
        r = np.sqrt((x - 15) * (x - 15) + (y - 15) * (y - 15))
        a[1, y, x] = np.exp((r - 10) * (r - 10) / -10)
for x in range(31):
    for y in range(31):
        a[2, y, x] = np.exp(((x - 15) * (x - 15)) / -10)

fig, axs = plt.subplots(nrows=4, ncols=3, subplot_kw={'xticks': [], 'yticks': []})
for i in range(3):        
    axs[0][i].imshow(a[i])

with open(outfile, 'w') as txt, open(labelfile, 'w') as labeltxt:
    for i in range(totnFrames):
        cluster = random.randint(0, 2)
        b = np.zeros((31, 31))
        for j in range(FramePresentationTime):
            for x in range(31):
                for y in range(31):
                    ch = '.' if random.random() > maxFrequency * a[cluster, y, x] else '@'
                    txt.write(ch)
                    if ch == '@':
                        b[y, x] += 1
            txt.write('\n')
            labeltxt.write(str(cluster))
            labeltxt.write('\n')
        if i < 9:
            axs[i // 3 + 1][i % 3].imshow(b)

plt.tight_layout()
plt.show()
