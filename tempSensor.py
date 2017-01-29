#!/usr/bin/env python
#
# Adadpted from Michael Saunby. April 2013
#
import pexpect
import sys
import time

from lib.libLog import initLogging


def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t)
        pass
    return t


def calcTemp(rTemp):
    return rTemp / 4.0 * 0.03125

tempSensorLogger = initLogging('/var/log/fireV3/tempSensor.log')

#bluetooth_adr = sys.argv[1] # 'A0:E6:F8:AF:3C:06'
bluetooth_adr = "A0:E6:F8:AF:3C:06"
print "connecting to " + bluetooth_adr 

startUSB = pexpect.spawn ('sudo hciconfig hci0 up') 
tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
tool.expect('\[LE\]>')
print "Preparing to connect. You might need to press the side button..."
tool.sendline('connect')
# test for success of connect
tool.expect('Connection successful')
print "Connection successful"
# Switch on IR Temp sensor
#tool.sendline('char-write-cmd 0x0027 01')
tool.expect('\[LE\]>')
while True:
    # time.sleep(5)
    # Switch on IR Temp sensor
    tool.sendline('char-write-cmd 0x0027 01')
    time.sleep(1)
    # Read the temp/humidity data
    tool.sendline('char-read-hnd 0x0024')
    tool.expect('descriptor: .*')
    rVal = tool.after.split()
    #print "Raw data : " + str(rVal)
    rObjTemp = floatfromhex(rVal[2] + rVal[1])
    #print "Raw obj temp in decimal: " + str (rObjTemp)

    rAmbTemp = floatfromhex(rVal[4] + rVal[3])
    # print "Humidity in decimal: " + str (rAmbTemp)

    objTemp = calcTemp (rObjTemp)
    ambTemp = calcTemp (rAmbTemp)

    #print "Obj: " + "%.2f C" % objTemp + " Amb:  " + "%.2f " % ambTemp + "%"
    tempSensorLogger.debug ( "Obj: " + "%.2fC" % objTemp + " Amb:  " + "%.2fC" % ambTemp)
    # Switch off the temp sensor
    tool.sendline('char-write-cmd 0x0027 00')
    time.sleep(3)
