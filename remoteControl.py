#!/usr/bin/env python

# Read from remote control via flirc

# Requires the following:
# sudo apt-get install python-dev python-pip gcc
# sudo pip install evdev


# modules to read from the flirc
from evdev import InputDevice, categorize, ecodes

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
                    print ("code: " + str(event.code))

# Next - put me in my own thread and call me from controlFire

if __name__ == "__main__":
    print "Executing remoteControl.py test code"
    startRemoteScanning()
