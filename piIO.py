#!/usr/bin/env python

# May move this in to the library

# Drive Raspberry Pi hardware

# Requires the following:


import time
from lib.libLog import initLogging

# modules to read/write to Pi Hardware
import RPi.GPIO as GPIO

ON = True
OFF = False

# GPIO PINs
OUT_RELAY_PIN = 18

def init_GPIO():
    GPIO.setwarnings(False)
    GPIO.setmode (GPIO.BCM)

    GPIO.setup(OUT_RELAY_PIN, GPIO.OUT)

def switch_fire_relay (off_or_on):
    if off_or_on == ON:
        GPIO.output (OUT_RELAY_PIN, True)
        piHwIoLogger.info ("Relay is ON")
    else:
        GPIO.output (OUT_RELAY_PIN, False)
    	piHwIoLogger.info ("Relay is OFF")
     

init_GPIO()

piHwIoLogger = initLogging('/var/log/fireV3/piIO.log')

if __name__ == "__main__":
    print "Executing remoteControl.py test code"
    print "Switch relay on: "
    switch_fire_relay(ON)
    print "Eait for 5 seconds"
    time.sleep(5)
    print "Switch relay off: "
    switch_fire_relay(OFF)  
