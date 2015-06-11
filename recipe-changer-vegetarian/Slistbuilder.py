#!/usr/bin/env python
import sys
spicefile = sys.argv[1]
newspicefile = sys.argv[2]
spicelist = []

with open (spicefile) as f:
    for line in f:
        spice = line.split("\t")
        spicelist.append(spice)

newspicelist = []

with open (newspicefile) as f:
    for line in f:
        spice = line.split("\t")
        name = spice[0].strip()
        newspicelist.append(name)

slist = []
for i in range(len(spicelist)):
    for x in range(2):
        slist.append(spicelist[i][x].strip())

for i in range(len(newspicelist)):
    if (newspicelist[i] not in slist):
        add = (newspicelist[i],'','','')
        spicelist.append(add)

f = open(spicefile, 'w')
for i in range(len(spicelist)):
    for x in range(4):
        f.write(str(spicelist[i][x]))
        f.write('\t')
    f.write('\n')