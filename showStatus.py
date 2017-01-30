#!/usr/bin/env python

# Loop reading the contents of showStatus.txt. Push data
# to the alphanumeric display based on the contents.

import time
from lib.libFile import readDataFromFile
from lib.libConstants import UI_SLEEP_TIME
from piIO import printMessage, printNumberMessage

def startShowStatus ():
    while True:
        dataToShow = readDataFromFile('datafiles/showStatus.txt')
 #       print dataToShow
        if dataToShow == "MEASURED":
            data = readDataFromFile('datafiles/measuredTemperature.txt')
            print "Temp: " +  data
            # remove the decimal point as it takes up a whole character
            # data = data.replace(".","")
            data = 'm' + data
            printNumberMessage (data)
        elif dataToShow == "DESIRED":
            data = readDataFromFile ('datafiles/desiredTemperature.txt')
            data = 'd' + data
            printMessage (data)
        elif dataToShow == "BLANK":
            printMessage ('    ')
        elif dataToShow == "CONTROL":
                data = readDataFromFile ('datafiles/controlStatus.txt')
                printMessage (data)
        elif dataToShow == "STATUS":
            data = readDataFromFile ('datafiles/statusStatus.txt')
            printMessage (data)
        else:
            pass #error
        time.sleep(UI_SLEEP_TIME)

def OLD_startShowStatus ():
    while True:
        data = readDataFromFile('datafiles/measuredTemperature.txt')
        print str(data)
        printMessage (data)
        time.sleep(1)

if __name__ == "__main__":
    startShowStatus ()
