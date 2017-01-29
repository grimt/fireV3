#!/usr/bin/env python

# The main script to control the fire

import time
import signal
import os
from threading import Thread, Event

from lib.libFile import readDataFromFile
from lib.libLog import initLogging
from remoteControl import startRemoteScanning
from tempOverride import startTemperatureOverride
from tempSensor import startTempSensor

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
            # Switch off fire at relay

    def switchFireOn(self):
        if self.fireState == FIRE_OFF:
            print 'switch fire on'
            self.fireState = FIRE_ON
            # Switch on fire at relay

    def runAutoControlAlgorithm (self):
        controlFireLogger.debug ('Hysteresis: current state: ' + str (self.fireState)\
         + ' desired: ' + str (self.desiredTemperature) + ' Measured: ' + str (self.measuredTemperature))
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
        if self.fireState == FIRE_ON:
            print "Fire is on"
        else:
            print "Fire is off"

        print "Desired temperature : " + str(self.desiredTemperature)
        print "Measured temperature: " + str(self.measuredTemperature)
        print "Control Status      : " + self.controlStatus
        print "Time Override       : " + self.timeOverride

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
 temperatureSensor.start()

try:
    while True:

        fire.desiredTemperature = readDataFromFile('datafiles/desiredTemperature.txt')
        fire.measuredTemperature = readDataFromFile('datafiles/measuredTemperature.txt')
        fire.controlStatus = readDataFromFile('datafiles/controlStatus.txt')
        fire.timeOverride = readDataFromFile('datafiles/timeOverride.txt')

        fire.runControlAlgorithm()

        time.sleep(1)
# TODO - make this exception more specific
except KeyboardInterrupt:
    fire.switchFireOff()
    controlFireLogger.debug ('Switch fire OFF Program Terminates')

# Next implement hardware I/O for relay
