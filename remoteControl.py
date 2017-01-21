#!/usr/bin/env python

# Read from remote control via flirc

# Requires the following:
# sudo apt-get install python-dev python-pip gcc
# sudo pip install evdev


# modules to read from the flirc
from evdev import InputDevice, categorize, ecodes
from libFile import readDataFromFile, writeDataToFile

# Remote control Key definitions
REMOTE_KEY_NONE = 0
REMOTE_KEY_RED = 2
REMOTE_KEY_GREEN = 3
REMOTE_KEY_YELLOW = 4
REMOTE_KEY_BLUE = 5

def updateOn ():
    writeDataToFile ('datafiles/controlStatus.txt', 'ON')

def updateOff ():
    writeDataToFile ('datafiles/controlStatus.txt', 'OFF')

def updateAuto():
    writeDataToFile ('datafiles/controlStatus.txt', 'AUTO')

def toggleDisplayMode():
    # display measured -> display desired -> display off
    currentStatus = readDataFromFile('datafiles/displayStatus.txt')
    if currentStatus == 'MEASURED':
        writeDataToFile ('datafiles/displayStatus.txt', 'DESIRED')
    elif currentStatus == 'DESIRED':
        writeDataToFile ('datafiles/displayStatus.txt', 'OFF')
    elif currentStatus == 'OFF'
        writeDataToFile ('datafiles/displayStatus.txt', 'MEASURED')
    else
        pass #error




dev = InputDevice ('/dev/input/event0')
def startRemoteScanning():
    for event in dev.read_loop():
        #
        # type should always be 1 for a keypress
        # code is the numeric value of the key that has been pressed
        # value 0 = key up, 1 = key down, 2 = key hold

        if event.type == ecodes.EV_KEY:
            # my_logger.debug (categorize(event))
            print ( 'type: ' + str (event.type) + ' code: ' + str (event.code) + ' value ' + str (event.value))
            if event.value == 0:  # key up
                if event.code == REMOTE_KEY_RED:
                    updateOn()
                elif event.code == REMOTE_KEY_GREEN:
                    updateOff()
                elif event.code == REMOTE_KEY_YELLOW:
                    updateAuto()
                elif event.code == REMOTE_KEY_BLUE:
                    toggleDisplayMode()
                elif event.code == REMOTE_KEY_NONE:
                    pass
                else
                    # TODO Up/DOWN for desired temperature
                    print "Code: " + str (event.code)

# Next - write data to files based on remote control key presses.

if __name__ == "__main__":
    print "Executing remoteControl.py test code"
    startRemoteScanning()
