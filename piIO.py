#!/usr/bin/env python

# May move this in to the library

# Drive Raspberry Pi hardware

# Requires the following:



from lib.libLog import initLogging
# modules to read/write to Pi Hardware




piHwIoLogger = initLogging('/var/log/fireV3/piIO.log')

if __name__ == "__main__":
    print "Executing remoteControl.py test code"
startRemoteScanning()
