#!/usr/bin/env python
# Library for Bluetooth functionality common accross all modules.

import bluetooth
import dbus

# from bluetooth.ble import DiscoveryService

# Test code
if __name__ == "__main__":
	print "Running Bluetooth test code"

	nearby_devices = bluetooth.discover_devices(lookup_names=True)
        print("found %d devices" % len(nearby_devices))

	for addr, name in nearby_devices:
    		print("  %s - %s" % (addr, name))
		if name == 'HTC Incredible S':
                	for services in bluetooth.find_service(address = addr):
						print " Name: %s" % (services["name"])
						print " Description: %s" % (services["description"])
						print " Protocol: %s" % (services["protocol"])
						print " Provider: %s" % (services["provider"])
						print " Port: %s" % (services["port"])
						print " Service id: %s" % (services["service-id"])
						print ""
						print ""


	# service = DiscoveryService()
	# devices = service.discover(2)

	# for address, name in devices.items():
    	# 	print("name: {}, address: {}".format(name, address))
