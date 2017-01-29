#!/usr/bin/env python

# Loop reading the contents of showStatus.txt. Push data
# to the alphanumeric display based on the contents.

from lib.libFile import readDataFromFile
from piIO import printMessage

def startShowStatus ():
    while True:
        dataToShow = readDataFromFile('datafiles/showStatus.txt')
        if dataToShow == "MEASURED":
            data = readDataFromFile('datafiles/measuredTemperature.txt')
            printMessage (data)
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
