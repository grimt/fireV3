#!/usr/bin/env python

# Loop reading the contents of showStatus.txt. Push data
# to the alphanumeric display based on the contents.

import time
from lib.libFile import readData
from lib.libConstants import UI_SLEEP_TIME
from piIO import printMessage, printNumberMessage, setBrightness

def startShowStatus ():
    while True:
        # First set the brightness
        try:
            brightness = int (readData ('datafiles/alphaNumBrightness.txt'))
            setBrightness (brightness)
        except ValueError:
            print "Value error reading: " + readData ('datafiles/alphaNumBrightness.txt')

        dataToShow = readData('datafiles/showStatus.txt')
 #       print dataToShow
        if dataToShow == "MEASURED":
            data = readData('datafiles/measuredTemperature.txt')
            data = 'm' + data
            # Take care of the decimal point
            printNumberMessage (data)
        elif dataToShow == "DESIRED":
            data = readData ('datafiles/desiredTemperature.txt')
            data = 'd' + data
            printMessage (data)
        elif dataToShow == "BLANK":
            printMessage ('    ')
        elif dataToShow == "CONTROL":
                data = readData ('datafiles/controlStatus.txt')
                printMessage (data)
        elif dataToShow == "SYSTEM":
            data = readData ('datafiles/systemStatus.txt')
            printMessage (data)
        elif dataToShow == "BATTERY":
            data = readData ('datafiles/batteryLife.txt')
            data = 'b' + data
            printMessage (data)
        else:
            pass #error
        time.sleep(UI_SLEEP_TIME)

def OLD_startShowStatus ():
    while True:
        data = readData('datafiles/measuredTemperature.txt')
        print str(data)
        printMessage (data)
        time.sleep(1)

if __name__ == "__main__":
    startShowStatus ()
