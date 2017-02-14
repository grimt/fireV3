#!/usr/bin/env python

# Read from remote control via flirc

# Requires the following:
# sudo apt-get install python-dev python-pip gcc
# sudo pip install evdev


from lib.libLog import initLogging
# modules to read from the flirc
from evdev import InputDevice, categorize, ecodes
from lib.libFile import readData, writeData

# Remote control Key definitions
REMOTE_KEY_NONE = 0
REMOTE_KEY_RED = 3
REMOTE_KEY_GREEN = 2
REMOTE_KEY_YELLOW = 4
REMOTE_KEY_BLUE = 5
REMOTE_KEY_UP = 103
REMOTE_KEY_DOWN = 108
LED_BRIGHTNESS_KEY_UP = 24
LED_BRIGHTNESS_KEY_DOWN = 38

def updateOn ():
    writeData ('datafiles/controlStatus.txt', 'ON')
    writeData ('datafiles/showStatus.txt', "CONTROL")

def updateOff ():
    writeData ('datafiles/controlStatus.txt', 'OFF')
    writeData ('datafiles/showStatus.txt', "CONTROL")

def updateAuto():
    writeData ('datafiles/controlStatus.txt', 'AUTO')
    # Default desired temperature to 19 when moving to AUTO
    writeData('datafiles/desiredTemperature.txt', str(19))
    writeData ('datafiles/showStatus.txt', "CONTROL")

def toggleDisplayMode():
    # display measured -> display desired -> display off
    currentStatus = readData('datafiles/showStatus.txt')
    if currentStatus == "MEASURED":
        writeData ('datafiles/showStatus.txt', "DESIRED")
    elif currentStatus == "DESIRED":
        writeData ('datafiles/showStatus.txt', "BLANK")
    elif currentStatus == "BLANK":
        writeData ('datafiles/showStatus.txt', "CONTROL")
    elif currentStatus == "CONTROL":
        writeData ('datafiles/showStatus.txt', "BATTERY")
    elif currentStatus == "BATTERT":
        writeData ('datafiles/showStatus.txt', "SYSTEM")
    elif currentStatus == "SYSTEM":
        writeData ('datafiles/showStatus.txt', "MEASURED")
    else:
        pass #error

def desiredTemperatureUp():
    try:
        currentTemp = int (readData('datafiles/desiredTemperature.txt'))
        currentTemp += 1
        writeData('datafiles/desiredTemperature.txt', str(currentTemp))
        writeData ('datafiles/showStatus.txt', "DESIRED")
    except:
        pass

def desiredTemperatureDown():
    try:
        currentTemp = int (readData('datafiles/desiredTemperature.txt'))
        if currentTemp > 0:
            currentTemp -= 1
            writeData('datafiles/desiredTemperature.txt', str(currentTemp))
            writeData ('datafiles/showStatus.txt', "DESIRED")
    except:
        pass

def ledBrightnessUp():
    try:
        currentBrightness = int (readData('datafiles/alphaNumBrightness.txt'))
        if currentBrightness < 15:
            currentBrightness += 1
            writeData('datafiles/alphaNumBrightness.txt', str(currentBrightness))
    except:
        pass

def ledBrightnessDown():
    try:
        currentBrightness = int (readData('datafiles/alphaNumBrightness.txt'))
        if currentBrightness > 0:
            currentBrightness -= 1
            writeData('datafiles/alphaNumBrightness.txt', str(currentBrightness))
    except:
        pass

dev = InputDevice ('/dev/input/event0')
def startRemoteScanning():
    for event in dev.read_loop():
        #
        # type should always be 1 for a keypress
        # code is the numeric value of the key that has been pressed
        # value 0 = key up, 1 = key down, 2 = key hold

        if event.type == ecodes.EV_KEY:
            # my_logger.debug (categorize(event))
            if event.value == 0:  # key up
                remoteControlLogger.debug ( 'type: ' + str (event.type) + \
                ' code: ' + str (event.code) + ' value ' + str (event.value))
                # Pressing any key switches of the time override
                writeData ('datafiles/timeOverride.txt', 'OFF')

                if event.code == REMOTE_KEY_RED:
                    updateOn()
                elif event.code == REMOTE_KEY_GREEN:
                    updateOff()
                elif event.code == REMOTE_KEY_YELLOW:
                    updateAuto()
                elif event.code == REMOTE_KEY_BLUE:
                    toggleDisplayMode()
                elif event.code == REMOTE_KEY_UP:
                    desiredTemperatureUp()
                elif event.code == REMOTE_KEY_DOWN:
                    desiredTemperatureDown()
                elif event.code == REMOTE_KEY_NONE:
                    pass
                elif event.code == LED_BRIGHTNESS_KEY_UP:
                    ledBrightnessUp()
                elif event.code == LED_BRIGHTNESS_KEY_DOWN:
                    ledBrightnessDown()
                else:
                    # TODO Up/DOWN for desired temperature
                    print "Code: " + str (event.code)


remoteControlLogger = initLogging('/var/log/fireV3/remoteControl.log')

if __name__ == "__main__":
    print "Executing remoteControl.py test code"
    startRemoteScanning()
