#!/usr/bin/env python

def retrievelist(lfile):
    mylist = []
    with open (lfile) as f:
        for line in f:
            items = line.split(",") #pushes line into an array by , seperation which is how our excel files are saved
            for t in items:
                t = t.strip().lower() ## remove spaces and newline characters etc.
                if (t):
                    mylist.append(t) #push to array
    return mylist
def addtolist(lfile, word): ##takes the filename that the list was drawn from and appends the new word
    with open (lfile, 'a') as f:
        f.write(word + "\n") ##each new one added is on a new line
    return 0
proteins = retrievelist('lists/proteins.csv')
actions = retrievelist('lists/actions.csv')
equipment = retrievelist('lists/equipment.csv')
measurements = retrievelist('lists/measurements.csv')
vegetables = retrievelist('lists/vegetables.csv')
fruits = retrievelist('lists/fruits.csv')

