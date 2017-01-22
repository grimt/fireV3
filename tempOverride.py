#!/usr/bin/env python

# The fire should be switched off unless it is between 4pm and 10pm
# This task will check the time at half hour intervals and switch the
# fire off unless the time is within the range specified above.
# Note the fire can be switched on again by the remote but it will
# be switched off again in the next half hour

import os
import sys

import time
import datetime

from lib.libLog import initLogging
from lib.libFile import  writeDataToFile


def updateOff ():
    writeDataToFile ('datafiles/controlStatus.txt', 'OFF')

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def startTemperatureOverride():
    while True:
    	localtime = datetime.datetime.time(datetime.datetime.now())
    	start = datetime.time(16, 0, 0) # 4pm
    	end = datetime.time(22, 0, 0) # 10pm

    	if not (time_in_range (start, end, localtime)):
            # switch the fire off
            tempOverrideLogger.warning ('Switch fire OFF as outside time range at: ' + str(localtime))
            updateOff ()
            # Tell the world we are in override mode.
            writeDataToFile ('datafiles/timeOverride.txt', 'ON')

        time.sleep (60 * 30) # check again in 30 minutes
        # time.sleep (30) # use 30 seconds for debug purposes



tempOverrideLogger = initLogging('/var/log/fireV3/tempOverride.log')

if __name__ == "__main__":
    print "Executing tempOverride.py test code"
    startTemperatureOverride()
