#!/usr/bin/env python

# The main script to control the fire

class cFire:
    def __init__(self):
        self.desiredTemperature = 0
        self.measuredTemperature = 0
        self.control = "manual" # manual or automatic
        self.timeOverride = False


fire = cFire()

# Next - while loop reading data from files.
