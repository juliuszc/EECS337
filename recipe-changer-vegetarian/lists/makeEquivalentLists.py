#!/usr/bin/python

import sys

if len(sys.argv) == 2:
    filename = sys.argv[1]
    f = open(filename, 'r')
    ret = []
    for line in f:
    	ourDict = {}
    	line2 = line.strip().split(',')
    	ourDict['american'] = line2[0].lower().strip()
    	ourDict['italian'] = line2[1].lower().strip()
    	ourDict['asian'] = line2[2].lower().strip()
    	ourDict['mexican'] = line2[3].lower().strip()
    	ret.append(ourDict)
    print ret
else:
	print "makeEquivalentList requires an input of a CSV file"
