#!/usr/bin/python

import sys

if len(sys.argv) == 2:
    filename = sys.argv[1]
    f = open(filename, 'r')
    arr = '{'
    for line in f:
    	line2 = line.strip().split(',')
    	arr += '"' + line2[0].strip().lower() + '": "' + line2[1].strip().lower() + '", '
    arr = arr[0:-2] + '}'
    print arr
else:
	print "csv2dict requires an input of a CSV file"
