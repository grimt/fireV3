#!/usr/bin/env python
# Library for functionality common accross all modules.

# Data files functionality

def writeDataToFile (filename, data):
# filename:   string - full path to file
# data:       string - data to write
# exceptions: log and continue
    try:
        f = open (filename, 'wt')
        f.write (data)
        f.close ()

    except IOError:
        print ("Cant open file " + filename + " for writing")

def readDataFromFile(filename):
    data = ''
    try:
        f = open (filename,'rt')
        data = f.read ()
        f.close ()
    except IOError:
        print("Cant open file desired_temperature.txt for reading")

    return data

# Test code
if __name__ == "__main__":
    print "Executing test code:"
    writeDataToFile ('datafiles/testFile.txt', 'BOLLARDS')
    print readDataFromFile ('datafiles/testFile.txt')

    # Next - try writing and reading numbers as strings then converting back to numbers
