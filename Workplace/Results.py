import csv
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple
import numpy as np
import statistics
import bisect

file = "monitoring.3.csv"   # Here, the monitoring file name should be specified

sec = []
CharTime = []
ThresholdExcessIncrementMultiplier = []
AbsRefT = []
WINC = []
Inh = []
minW = []
maxW = []
SectionName = []

secint = []
SectionIntensity = namedtuple('SectionIntensity', ['sec', 'tact', 'relfre'])
lin = []
Link = namedtuple('Link', 'tact,neu,type,indsyn,Is_pla,delay,src,effw,basew,W')
tact = []
neusec = []
migrations = []
ReceptorBounds = []

# Parse monitoruing file

with open(file, newline = '') as fil:
    bHeader = True
    csr = csv.reader(fil)
    for row in csr:
        if bHeader:
            bHeader = False
        elif row[0] == "secsta":
            sec.append(int(row[1]))
            CharTime.append(float(row[2]))
            ThresholdExcessIncrementMultiplier.append(row[5])
            AbsRefT.append(float(row[6]))
            WINC.append(float(row[7]))
            Inh.append(float(row[8]))
            minW.append(float(row[9]))
            maxW.append(float(row[10]))
            SectionName.append(row[12])
        elif row[0] == "rec":
            ReceptorBounds.append([int(row[1]), int(row[2])])
        elif row[0] == "secint":
            if float(row[2]) >= 0:
                secint.append(SectionIntensity(int(row[2]), int(row[1]), float(row[3])))
        elif row[0] == "lin":
            lin.append(Link(float(row[1]), int(row[2]), float(row[3]), float(row[4]), float(row[5]) != 0, float(row[6]), int(row[7]), float(row[8]), float(row[9]), float(row[10])))
        elif row[0] == "neu->sec":
            tac = int(row[1])
            neu = int(row[2])
            s = int(row[3])

            # It is assumed that the 1st neu->sec section is ordered ny neu

            if len(tact) == 0 or tac != tact[-1]:
                tact.append(tac)
                neusec.append([] if tac == 0 else [-1 for i in range(len(neusec[0]))])
                migrations.append(0)
            if tac == 0:
                neusec[-1].append(s)
            else:
                neusec[-1][neu] = s
        elif row[0] == "neudyn":
            migrations[-1] += 1

nSectionsperNetwork = len(sec)
print('total number of sections ', len(sec))

SecInt = {}
nrows = round(np.sqrt(nSectionsperNetwork / 2))
ncols = (nSectionsperNetwork - 1) // nrows + 1
matplotlib.rc('font', size=15)
fig, axs = plt.subplots(nrows, ncols)
i = 0
if nrows == 1 and ncols == 1:
    s = sec[0]
    x = [t.tact for t in secint if t.sec == s]
    y = [t.relfre * 1000 for t in secint if t.sec == s]
    SecInt[s] = statistics.mean(y)
    axs.set_title(SectionName[i])
    axs.plot(x, y, linewidth = 1)
    axs.set(xticks=[])
else:
    for ax in axs.flat:
        if i < len(sec):
            s = sec[i]
            x = [t.tact for t in secint if t.sec == s]
            y = [t.relfre * 1000 for t in secint if t.sec == s]
            SecInt[s] = statistics.mean(y)
            ax.set_title(SectionName[i])
            ax.plot(x, y, linewidth = 1)
            ax.set(xticks=[])
        i += 1
plt.title('Section firing frequency (Hz)')
plt.show()

print("mean section intensity:")
print(SecInt)

effw = [t.effw if t.type == 3 else t.W for t in lin]

i = 0
deffw_sum = {}
tactNo = -1
guess_shift = -1
maxNLinksofThisType = {}

NLinksofThisType = {}

print("Link data processing...")
cnt = 0
lastneu = -1
while i <= len(lin):
    end = i == len(lin)
    if i == 0 or end or lin[i].tact != lin[i - 1].tact:
        guess_shift = cnt
        cnt = 0
    if end or lin[i].Is_pla:
        if end or lin[i].neu != lastneu:
            for str, l in NLinksofThisType.items():
                if l > maxNLinksofThisType.setdefault(str, 0):
                    maxNLinksofThisType[str] = l
            if not end:
                lastneu = lin[i].neu
                NLinksofThisType.clear();
        if not end:
            if tactNo < 0 or lin[i].tact != tact[tactNo]:
                tactNo += 1
                print('Now tact %d is processed' % tact[tactNo])
            strsecfrom = "R%d" % (bisect.bisect_left(ReceptorBounds, [-lin[i].src - 1, 1000000000]) - 1,) if lin[i].src < 0 else "%d" % (neusec[tactNo][lin[i].src - 1],)
            secto = neusec[tactNo][lin[i].neu]
            strLink = strsecfrom + '->' + SectionName[secto]
            if tactNo == 0 and deffw_sum.get(strLink) == None:
                deffw_sum[strLink] = []
            if tactNo > 0:
                if len(deffw_sum[strLink]) < tactNo:
                    deffw_sum[strLink].append(0)
                if i - guess_shift < 0:
                    guess_shift = i
                if lin[i - guess_shift].neu < lin[i].neu:
                    while lin[i - guess_shift].neu < lin[i].neu:
                        guess_shift -= 1
                elif lin[i - guess_shift].neu > lin[i].neu:
                    while lin[i - guess_shift].neu > lin[i].neu:
                        guess_shift += 1
                if lin[i - guess_shift].src > lin[i].src:
                    while lin[i - guess_shift].src > lin[i].src and lin[i - guess_shift].neu == lin[i].neu:
                        guess_shift -= 1
                elif lin[i - guess_shift].src < lin[i].src:
                    while lin[i - guess_shift].src < lin[i].src and lin[i - guess_shift].neu == lin[i].neu:
                        guess_shift += 1
                if lin[i - guess_shift].src == lin[i].src and lin[i - guess_shift].neu == lin[i].neu:
                    deffw_sum[strLink][-1] += abs(effw[i] - effw[i - guess_shift])
                else:
                    deffw_sum[strLink][-1] += abs(effw[i])
            if strsecfrom[0] != 'R':
                strsecfrom = SectionName[neusec[tactNo][lin[i].src - 1] % nSectionsperNetwork]
            secto = secto % nSectionsperNetwork
            strLink = strsecfrom + '->' + SectionName[secto]
            NLinksofThisType.setdefault(strLink, 0)
            NLinksofThisType[strLink] += 1
    cnt += 1
    i += 1

print("Maximum number (in the whole history) of links between sections")
print(maxNLinksofThisType)

fig, axs = plt.subplots(1, 1, figsize = (10, 3))
i = 0
for d in deffw_sum.keys():
    if max(deffw_sum[d]) > 0:
        axs.plot(tact[1:len(deffw_sum[d])+1], deffw_sum[d], label = d, linewidth = 1)
leg = axs.legend(loc = 'best', ncol = 2)
leg.get_frame().set_alpha(0.5)
i += 1
plt.title('Weight change dynamics')
plt.show()
