#!/usr/bin/python

import sys
import time
import smbus

I2C_CHANNEL = 1
I2C_ADDRESS = 0x39

class TSL2561:
    def __init__(self):
        self.ch   = I2C_CHANNEL
        self.addr = I2C_ADDRESS
        self.bus  = smbus.SMBus(self.ch)

    def initialize(self):
        self.bus.write_i2c_block_data(self.addr, 0x80, [0x03])
	time.sleep(0.5)

    def getVisible(self):
        data = self.bus.read_i2c_block_data(self.addr, 0xac, 2)
        raw  = data[1] << 8 | data[0]
        return raw

    def getInfrared(self):
        data = self.bus.read_i2c_block_data(self.addr, 0xae, 2)
        raw  = data[1] << 8 | data[0]
        return raw

    def getValue(self):
	visible  = self.getVisible()
        infrared = self.getInfrared()

        if float(visible) == 0:
            ratio = 9999;
        else:
            ratio = infrared / float(visible)

	# get Lux
        if ratio >= 0 and ratio <= 0.52:
            lux = (0.0315 * visible) - (0.0593 * visible * (ratio ** 1.4))
        elif ratio <= 0.65:
            lux = (0.0229 * visible) - (0.0291 * infrared)
        elif ratio <= 0.80:
            lux = (0.0157 * visible) - (0.018 * infrared)
        elif ratio <= 1.3:
            lux = (0.00338 * visible) - (0.0026 * infrared)
        else:
            lux = 0

        return lux

def getUsage():
    return "Usage: " + sys.argv[0] + " init | get"

if __name__ == "__main__":
    sensor = TSL2561()

    if len(sys.argv) == 2:
        if sys.argv[1] == "init":
            sensor.initialize()
        elif sys.argv[1] == "get":
            print "%.3f" % sensor.getValue()
        else:
            sys.exit(getUsage())
    else:
        sys.exit(getUsage())

sys.exit(0)

