#!/usr/bin/env python

# The main script to control the fire

import time
import signal
import os
from threading import Thread, Event

from lib.libFile import readDataFromFile
from lib.libLog import initLogging
from remoteControl import startRemoteScanning

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

controlFireLogger = initLogging('/var/log/fireV3/controlFire.log')

remoteControlThread = Thread(target=startRemoteScanning, args=())
remoteControlThread.daemon = True
remoteControlThread.start()

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
