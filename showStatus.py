#!/usr/bin/env python

# Loop reading the contents of showStatus.txt. Push data
# to the alphanumeric display based on the contents.

import time
from lib.libFile import readDataFromFile, writeDataToFile # writeData will go after debugging
from piIO import printMessage

# Next: work out why reading from string test is failing
def startShowStatus ():
    while True:
        writeDataToFile ('datafiles/showStatus.txt')
        dataToShow = readDataFromFile('datafiles/showStatus.txt')
#        print dataToShow
        if dataToShow == "MEASURED":
            print "True"
            data = readDataFromFile('datafiles/measuredTemperature.txt')
            print "Temp: " +  data
            printMessage (str(data))
            pass
        elif dataToShow == "DESIRED":
            pass
        elif dataToShow == "BLANK":
            printMessage ('    ')
        elif dataToShow == "CONTROL":
            pass
        elif dataToShow == "STATUS":
            pass
        else:
            pass #error
        time.sleep(1)

def OLD_startShowStatus ():
    while True:
        data = readDataFromFile('datafiles/measuredTemperature.txt')
        print str(data)
        printMessage (data)
        time.sleep(1)

if __name__ == "__main__":
    startShowStatus ()
