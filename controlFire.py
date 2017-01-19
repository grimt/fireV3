#!/usr/bin/env python

# The main script to control the fire

import time
import signal
import os
from lib.libFile import readDataFromFile
import logging
import logging.handlers

def init_logging():
    LOG_FILENAME = '/var/log/fireV3/controlFire.log'
    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s  %(message)s')

    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler( LOG_FILENAME, maxBytes=90000, backupCount=5)
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    my_logger.debug ('Start logging')
    return my_logger

class cFire:
    def __init__(self):
        self.desiredTemperature = 0
        self.measuredTemperature = 0
        self.manualControl = "off" # manual or automatic
        self.timeOverride = "off"

    def printDebug(self):
        print "Desired temperature : " + str(self.desiredTemperature)
        print "Measured temperature: " + str(self.measuredTemperature)
        print "Manual Control      : " + self.manualControl
        print "Time Override       : " + self.timeOverride


fire = cFire()
print 'My PID is:', os.getpid() # Remove after initial debug or move to a log

# For debugging purposes, send kill -USR1 <pid> to see classes internals
def receiveSignal(signum, stack):
    fire.printDebug()
signal.signal(signal.SIGUSR1, receiveSignal)

controlFireLogger = init_logging()

try:
    while True:

        fire.desiredTemperature = readDataFromFile('datafiles/desiredTemperature.txt')
        fire.measuredTemperature = readDataFromFile('datafiles/measuredTemperature.txt')
        fire.manualControl = readDataFromFile('datafiles/manualControl.txt')
        fire.timeOverride = readDataFromFile('datafiles/timeOverride.txt')

        # Next: Run the control algorithm

        time.sleep(1)
# TODO - make this exception more specific
except KeyboardInterrupt:
    # switch_fire(OFF)
    controlFireLogger.debug ('Switch fire OFF Program Terminates')
