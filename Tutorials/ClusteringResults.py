# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 12:02:46 2023

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt

labelfile = "../Workplace/cluster_labels.txt"
protocolfile = "../Workplace/spikes.3.txt"

step = 300

labels = []
protocol = []
a = [[[] for i in range(3)] for j in range(3)]

with open(labelfile, newline = '') as labeltxt:
    for line in labeltxt:
        labels.append(int(line))    
with open(protocolfile, newline = '') as txt:
    for line in txt:
        protocol.append(line)
        
counts = np.zeros((3, 3))
for ite in range(len(labels)):
    for neuron in range(3):
        if protocol[ite][neuron] == '@':
            counts[neuron,labels[ite]] += 1
    if ite % step == step - 1:
        for neuron in range(3):
            for cluster in range(3):
                a[neuron][cluster].append(counts[neuron, cluster])
        counts = np.zeros((3, 3))
        
fig, axs = plt.subplots(nrows=3, ncols=1)
for neuron in range(3):
    for cluster in range(3):
        axs[neuron].plot(a[neuron][cluster])
plt.show()