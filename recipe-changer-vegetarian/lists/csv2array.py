#!/usr/bin/python

import sys

if len(sys.argv) == 2:
    filename = sys.argv[1]
    f = open(filename, 'r')
    arr = '['
    for line in f:
    	line2 = line.strip().split(',')
    	for l in line2:
    		if l != '':
    		    arr += '"' + l.lower().strip() + '", '
    arr = arr[0:-2] + ']'
    print arr
else:
	print "csv2array requires an input of a CSV file"
