#!/usr/bin/env python
# Library for functionality common accross all modules.

# Data files functionality

def writeDataToFile (filename, data)
# filename:   string - full path to file 
# data:       string - data to write
# exceptions: log and continue
  try:
        f = open (filename, 'wt')
        f.write (data)
        f.close ()

  except IOError:
my_logger.exception ("Cant open file fire_status.txt for writing")
