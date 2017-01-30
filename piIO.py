#!/usr/bin/env python

# May move this in to the library

# Drive Raspberry Pi hardware

# Requires the following:


import time
from lib.libLog import initLogging
# See https://learn.adafruit.com/led-backpack-displays-on-raspberry-pi-and-beaglebone-black/usage
# for setting up the alphanumeric display
from Adafruit_LED_Backpack import AlphaNum4

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

def printMessage (message):
    # Pass in a 4 character string to be printed
    # on the alphanumeric display.
    pos = 0
    # Clear the display buffer.
    display.clear()
    # Print a 4 character string to the display buffer.
    display.print_str(message[pos:pos+4])
    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    display.write_display()
    
 def printNumberMessage (message):
    # Pass in a 4 character string to be printed
    # on the alphanumeric display.
    # Similar to printMessage but will interpret periods not as
    # characters but as decimal points associated with the previous character.
    pos = 0
    # Clear the display buffer.
    display.clear()
    # Print a 4 character string to the display buffer.
    display.print_number_str(message[pos:pos+4])
    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    display.write_display()   

# General IO
init_GPIO()

#Alphanumeric Display

# Create display instance on default I2C address (0x70) and bus number.
display = AlphaNum4.AlphaNum4()


# Initialize the display. Must be called once before using the display.
display.begin()

# Logging
piHwIoLogger = initLogging('/var/log/fireV3/piIO.log')

if __name__ == "__main__":
    print "Executing remoteControl.py test code"
    print "Switch relay on: "
    switch_fire_relay(ON)
    print "Wait for 1 seconds"
    time.sleep(1)
    print "Switch relay off: "
    switch_fire_relay(OFF)

    print "Now test the Alphanumeric"
    printMessage ('KISS')
    time.sleep(5)
    printMessage ('ME')
    time.sleep(5)
    printMessage ('NOW')
    time.sleep(5)
    printMessage ('    ')
    print "Done"
