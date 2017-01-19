#!/usr/bin/env python
# Library for File functionality common accross all modules.

import logging
import logging.handlers

def init_logging():
    LOG_FILENAME = '/var/log/firev3/libFile.log'
    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s  %(message)s')

    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler( LOG_FILENAME, maxBytes=90000, backupCount=5)
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    my_logger.debug ('Start logging')
    return my_logger

def writeDataToFile (filename, data):
# filename:   string - full path to file
# data:       string - data to write
# exceptions: log and continue
    try:
        f = open (filename, 'wt')
        f.write (data)
        f.close ()

    except IOError:
        libFileLogger.warning ("Cant open file " + filename + " for writing")

def readDataFromFile(filename):
    data = ''
    try:
        f = open (filename,'rt')
        data = f.read ()
        f.close ()
    except IOError:
        libFileLogger.warning ("Cant open file desired_temperature.txt for reading")

    return data

libFileLogger = init_logging()

# Test code
if __name__ == "__main__":
    print "Executing test code:"
    writeDataToFile ('../datafiles/testFile.txt', 'BOLLARDS')
    print readDataFromFile ('../datafiles/testFile.txt')

    # Writing and reading numbers as strings then converting back to numbers
    temp = 10
    temp = temp + 15
    writeDataToFile ('../datafiles/testFile.txt', str(temp))
    print int (readDataFromFile ('../datafiles/testFile.txt'))

    # Now floating point

    floatTemp = 24/7.0
    writeDataToFile ('../datafiles/testFile.txt', str(floatTemp))
    print float (readDataFromFile ('../datafiles/testFile.txt'))

    # Next add file specific logging for errors.
