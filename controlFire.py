#!/usr/bin/env python

# The main script to control the fire

import time
import signal
import os
from threading import Thread, Event

from lib.libFile import readData, writeData
from lib.libLog import initLogging
from lib.libConstants import CONTROL_SLEEP_TIME
from remoteControl import startRemoteScanning
from tempOverride import startTemperatureOverride
from tempSensor import startTempSensor
from showStatus import startShowStatus
from piIO import switchFireRelay

FIRE_ON = 1
FIRE_OFF = 0

class cFire:
    def __init__(self):
        self.desiredTemperature = 0
        self.measuredTemperature = 0.0
        self.controlStatus = "OFF" # Strings - OFF/ON/AUTO
        self.timeOverride = "OFF"  # Strings OFF/ON
        self.fireState = FIRE_OFF  # Integer FIRE_OFF/FIRE_ON

    def switchFireOff(self):
        if self.fireState == FIRE_ON:
            print 'Switch fire off'
            self.fireState = FIRE_OFF
            switchFireRelay (FIRE_OFF)

    def switchFireOn(self):
        if self.fireState == FIRE_OFF:
            print 'switch fire on'
            self.fireState = FIRE_ON
            switchFireRelay (FIRE_ON)

    def runAutoControlAlgorithm (self):
        #controlFireLogger.debug ('Hysteresis: current state: ' + str (self.fireState)\
         #+ ' desired: ' + str (self.desiredTemperature) + ' Measured: ' + str (self.measuredTemperature))
        try:
            if self.fireState == FIRE_OFF:
                if float(self.measuredTemperature) <= (float(self.desiredTemperature) - 0.5):
                    self.switchFireOn ()
                    controlFireLogger.debug ('Switch fire ON Desired: ' + str (self.desiredTemperature)\
                     + ' Measured: ' + str (self.measuredTemperature))
            else:
                try:
                    if float (self.measuredTemperature) >= (float(self.desiredTemperature)  + 0.5):
                        self.switchFireOff ()
                        controlFireLogger.debug ('Switch fire OFF Desired: ' + str (self.desiredTemperature)\
                            + ' Measured: ' + str (self.measuredTemperature))
                except:
                    controlFireLogger.exception ('ValueError exception' + str (self.measuredTemperature))
        except ValueError:
            controlFireLogger.exception ('ValueError exception' + str (self.measuredTemperature))

    def printDebug(self):
        try:
            f = open ("debug.txt", 'wt')
            if self.fireState == FIRE_ON:
                print "Fire is on"
                f.write("Fire is on")
            else:
                print "Fire is off"
                f.write("Fire is off")

            print "Desired temperature : " + str(self.desiredTemperature)
            f.write("Desired temperature : " + str(self.desiredTemperature))

            print "Measured temperature: " + str(self.measuredTemperature)
            f.write( "Measured temperature: " + str(self.measuredTemperature))

            print "Control Status      : " + self.controlStatus
            f.write "Control Status      : " + self.controlStatus

            print "Time Override       : " + self.timeOverride
            f.write("Time Override       : " + self.timeOverride)

            print "=============Datafiles==============="
            f.write("=============Datafiles===============")

            print "Control Status: " + readData('datafiles/controlStatus.txt')
            f.write "Control Status: " + readData('datafiles/controlStatus.txt')

            print "Desired temperature: " + readData('datafiles/desiredTemperature.txt')
            f.write "Desired temperature: " + readData('datafiles/desiredTemperature.txt')

            print "Measured Temperature: " + readData('datafiles/measuredTemperature.txt')
            f.write "Measured Temperature: " + readData('datafiles/measuredTemperature.txt')

            print "showStatus: " + readData('datafiles/showStatus.txt')
            f.write "showStatus: " + readData('datafiles/showStatus.txt')

            print "systemStatus: " + readData('datafiles/systemStatus.txt')
            f.write "systemStatus: " + readData('datafiles/systemStatus.txt')

            print "timeOverride: " + readData('datafiles/timeOverride.txt')
            f.write "timeOverride: " + readData('datafiles/timeOverride.txt')

            print "LED Brightness: " + readData('datafiles/alphaNumBrightness.txt')
            f.write "LED Brightness: " + readData('datafiles/alphaNumBrightness.txt')

            print "Override count: " + readData('datafiles/overrideCount.txt.txt')
            f.write "Override count: " + readData('datafiles/overrideCount.txt.txt')
            f.close ()





    def runControlAlgorithm(self):
        if self.controlStatus == 'OFF':
            self.switchFireOff()
        elif self.controlStatus == 'ON':
            self.switchFireOn()
        elif self.controlStatus == 'AUTO':
            self.runAutoControlAlgorithm()


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

temperatureOverrideThread = Thread(target=startTemperatureOverride, args=())
temperatureOverrideThread.daemon = True
temperatureOverrideThread.start()

temperatureSensorThread = Thread(target=startTempSensor, args=())
temperatureSensorThread.daemon = True
temperatureSensorThread.start()

# Control what gets sent to the alphanumeric display
showMessageThread = Thread(target=startShowStatus, args=())
showMessageThread.daemon = True
showMessageThread.start()

#TODO - Consider moving all logs and data files to a USB drive
writeData ('datafiles/showStatus.txt', "BLANK") # Default to nothing on the alphanumeric
writeData ('datafiles/systemStatus.txt', "GOOD") #BTEr Batt etc. show any errors
writeData ('datafiles/alphaNumBrightness.txt', "0") # 0 to 15
writeData ('datafiles/overrideCount.txt', "30") # Check if we need to do a time override every 30 minutes

try:
    while True:

        fire.desiredTemperature = readData('datafiles/desiredTemperature.txt')
        fire.measuredTemperature = readData('datafiles/measuredTemperature.txt')
        fire.controlStatus = readData('datafiles/controlStatus.txt')
        fire.timeOverride = readData('datafiles/timeOverride.txt')

        fire.runControlAlgorithm()

        time.sleep(CONTROL_SLEEP_TIME)
except KeyboardInterrupt:
    fire.switchFireOff()
    controlFireLogger.debug ('Switch fire OFF Program Terminates')
