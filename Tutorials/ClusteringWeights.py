
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import namedtuple
import matplotlib.colors as mcolors
import numpy as np

file = "../Workplace/monitoring.3.csv"
PictureSize = 31
ReceptorSectionBoundaries = PictureSize * PictureSize
nTargetClasses = 3

lin = []
Link = namedtuple('Link', 'tact,neu,type,indsyn,Is_pla,delay,src,effw,basew,W')
tact = []

# It is guaranteed that all records are ordered by tact

maxtact = 30000

with open(file, newline = '') as fil:
    bHeader = True
    csr = csv.reader(fil)
    for row in csr:
        if bHeader:
            bHeader = False
        elif row[0] == "lin":
            lin.append(Link(float(row[1]), int(row[2]), float(row[3]), float(row[4]), float(row[5]) != 0, float(row[6]), int(row[7]), float(row[8]), float(row[9]), float(row[10])))
        elif row[0] == "neu->sec":
            tac = int(row[1])
            if len(tact) == 0 or tac != tact[-1]:
                tact.append(tac)

effw = [t.effw if t.type == 3 and t.Is_pla else t.W for t in lin]

i = 0
tactNo = -1
NPlasticLinks = 0

RecField = []

print("Link data processing/...")
lastneu = -1
while i <= len(lin):
    end = i == len(lin)
    if end or lin[i].Is_pla:
        if end or lin[i].neu != lastneu:
            if not end:
                lastneu = lin[i].neu
        if not end:
            if tactNo < 0 or lin[i].tact != tact[tactNo]:
                RecField.append(np.zeros((nTargetClasses, PictureSize, PictureSize)))
                tactNo += 1
                print('Now tact %d is processed' % tact[tactNo])

            if  lin[i].src < ReceptorSectionBoundaries:
                ind = lin[i].src
                RecField[-1][lin[i].neu][ind % PictureSize][ind // PictureSize] = lin[i].W

            if tactNo == 0:
                NPlasticLinks += 1
    i += 1

print("number of plastic links: ", NPlasticLinks)

mpl.rc('font', size=10)
norm = mpl.colors.TwoSlopeNorm(vmin = -1000, vcenter = 0, vmax = 1000)

def draw_rec_fields(tac, rec_fields):
    indtact = tact.index(tac)
    for c in range(nTargetClasses):
        axes[c].clear()
        axes[c].imshow(rec_fields[indtact][c], cmap = 'seismic', norm=norm)
        axes[c].set_xticks([])
        axes[c].set_yticks([])

fig, axes = plt.subplots(1, nTargetClasses, subplot_kw={'aspect': 'equal'})
fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99, wspace=0.01, hspace=0.01)

draw_rec_fields(25000, RecField)
plt.show()
