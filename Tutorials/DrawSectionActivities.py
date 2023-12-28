# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 08:50:00 2023

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt

ExperimentNo = 2

FileNNC = "%d.nnc" % ExperimentNo
FileProtocol = "../Workplace/spikes.%d.txt" % ExperimentNo

def GetSectionBoundaries(fNNC):
    SectionBoundaries = []
    SectionNames = []
    SectionName = ""
    with open(fNNC, newline = '') as nnc:
        for line in nnc:
            try:
                i = line.index("<Section name=\"")
            except ValueError:
                try:
                    i = line.index("<n>")
                except ValueError:
                    continue
                else:
                    if len(SectionName) > 0:
                        SectionNames.append(SectionName)
                        s = line[i+3:]
                        j = int(s[:s.index("<")])
                        SectionBoundaries.append(j if len(SectionBoundaries) == 0 else SectionBoundaries[-1] + j)
            else:
                s = line[i+15:]
                SectionName = s[:s.index("\"")]
    return SectionNames, SectionBoundaries

def GetSectionActivities(Protocol, SectionBoundaries):
    ret = []
    with open(Protocol, newline = '') as pro:
        for line in pro:
            ret.append([line[(0 if i == 0 else SectionBoundaries[i - 1]) : SectionBoundaries[i]].count('@') for i in range(len(SectionBoundaries))])
    ret = np.asarray(ret)
    return ret
    
secname, secbou = GetSectionBoundaries(FileNNC)
act = GetSectionActivities(FileProtocol, secbou)
fig, ax = plt.subplots()
ax.plot(act)
ax.legend(secname)
plt.show()