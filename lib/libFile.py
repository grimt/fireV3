#!/usr/bin/env python
# Library for File functionality common accross all modules.

import logging
import logging.handlers

from libLog import initLogging

def writeDataToFile (filename, data):
# filename:   string - full path to file
# data:       string - data to write
# exceptions: log and continue
    try:
        f = open (filename, 'wt')
        f.write (data)
        f.close ()

    except IOError:
        libFileLogger.warning ("Cant open file " + filename + " for writing")

def appendDataToFile (filename, data):
# filename:   string - full path to file
# data:       string - data to write
# exceptions: log and continue
    try:
        f = open (filename, 'a')
        f.write (data)
        f.close ()

    except IOError:
        libFileLogger.warning ("Cant open file " + filename + " for writing")

def readDataFromFile(filename):
    data = ''
    try:
        f = open (filename,'rt')
        data = f.read ()
        f.close ()
    except IOError:
        libFileLogger.warning ("Cant open file desired_temperature.txt for reading")

    return data

def writeData (path, data):
    #print "Write to file: " + path
    path = '/home/pi/pycode/fireV3/' + path
    writeDataToFile (path, data)

def appendData (path, data):
    path = '/home/pi/pycode/fireV3/' + path
    appendDataToFile (path, data)

def readData (path):
    path = '/home/pi/pycode/fireV3/' + path
    return readDataFromFile (path)


libFileLogger = initLogging('/var/log/fireV3/libFile.log')

# Test code
if __name__ == "__main__":
    print "Executing test code:"
    writeDataToFile ('../datafiles/testFile.txt', 'BOLLARDS')
    print readDataFromFile ('../datafiles/testFile.txt')

    # Writing and reading numbers as strings then converting back to numbers
    temp = 10
    temp = temp + 15
    writeDataToFile ('../datafiles/testFile.txt', str(temp))
    print int (readDataFromFile ('../datafiles/testFile.txt'))

    # Now floating point

    floatTemp = 24/7.0
    writeDataToFile ('../datafiles/testFile.txt', str(floatTemp))
    print float (readDataFromFile ('../datafiles/testFile.txt'))

    # Next add file specific logging for errors.
