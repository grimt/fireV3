#!/usr/bin/env python
#
# Adadpted from Michael Saunby. April 2013
#
import pexpect
import sys
import time

from lib.libLog import initLogging
from lib.libFile import  writeData

#TODO - can we use int from hex
def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t)
        pass
    return t

def connectSensor (myTool):
    print "Preparing to connect. You might need to press the side button..."
    myTool.sendline('connect')
    j = myTool.expect([pexpect.TIMEOUT, 'Connection successful'], timeout=60)
    return j

def calcTemp(rTemp):
    return rTemp / 4.0 * 0.03125

def startTempSensor ():

    tempSensorLogger = initLogging('/var/log/fireV3/tempSensor.log')

    #bluetooth_adr = sys.argv[1] # 'A0:E6:F8:AF:3C:06'
    bluetooth_adr = "A0:E6:F8:AF:3C:06"
    print "connecting to " + bluetooth_adr

    startUSB = pexpect.spawn ('sudo hciconfig hci0 up')
    tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
    tool.expect('\[LE\]>')
    j = 1
    while True:
        #print "Preparing to connect. You might need to press the side button..."
        #tool.sendline('connect')
        # test for success of connect
        #j = tool.expect([pexpect.TIMEOUT, 'Connection successful'], timeout=60)

        j = connectSensor(tool)
        if j == 1:
            print "Connection successful"
            writeData ('datafiles/systemStatus.txt', "GOOD")
            tool.expect('\[LE\]>')
            goodConnection = True
            while goodConnection == True:
                # Switch on  Temp sensor
                tool.sendline('char-write-cmd 0x0027 01')
                time.sleep(1)
                # Read the temp data
                tool.sendline('char-read-hnd 0x0024')
                i = 1
                i = tool.expect([pexpect.TIMEOUT, 'descriptor: .*'], timeout=5)
                if i == 1:
                    rVal = tool.after.split()
                    rObjTemp = floatfromhex(rVal[2] + rVal[1])

                    rAmbTemp = floatfromhex(rVal[4] + rVal[3])

                    objTemp = calcTemp (rObjTemp)
                    ambTemp = calcTemp (rAmbTemp)

                    # print "Obj: " + "%.2f C" % objTemp + " Amb:  " + "%.2f " % ambTemp + "%"
                    #tempSensorLogger.debug ( "Obj: " + "%.2fC" % objTemp + " Amb:  " + "%.2fC" % ambTemp)
                    writeData ('datafiles/measuredTemperature.txt', "%.1f" % ambTemp)
                    # Now read the battery life
                    tool.sendline('char-read-hnd 0x001e')
                    k = tool.expect([pexpect.TIMEOUT, 'descriptor: .*'], timeout=5)
                    if k == 1:
                        rVal = tool.after.split()
                        #print "Battery: " + str(floatfromhex(rVal[1]))
                        writeData ('datafiles/batteryLife.txt', "%.0f" % floatfromhex(rVal[1]))
                    else:
                        goodConnection = False
                        writeData ('datafiles/systemStatus.txt', "BTEr")

                else:
                    print "Bad Connection"
                    goodConnection = False
                    writeData ('datafiles/systemStatus.txt', "BTEr")
                # Switch off the temp sensor
                tool.sendline('char-write-cmd 0x0027 00')
                time.sleep(1)
        else:
            print "Bad Connection"
            goodConnection = False
            writeData ('datafiles/systemStatus.txt', "BTEr")
