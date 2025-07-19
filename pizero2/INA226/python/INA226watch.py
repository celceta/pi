#!/usr/bin/env python3

# https://github.com/e71828/pi_ina226

import logging
from ina226 import INA226
from time import sleep
import urllib.request
from datetime import datetime

BASEURL = "https://iot.344.jp/put_multi.cgi?DEV=BTPV1&VAL=%.2f,%.2f,%.2f,%.2f,%.2f,%.2f"

class Average:

	arr = []

	def __init__(self, number_of_elements = 10):
		num = number_of_elements

	def add(newval):
		arr.insert(0, newval)
		del arr[num:]

	def getAverage():
		total = 0.
		for n in arr:
			total += n
		return n / arr.count()


if __name__ == "__main__":
	INA226_Battery = INA226(busnum=1, address=0x44, max_expected_amps=100, shunt_ohms=0.00075, log_level=logging.INFO)
	INA226_Pv1     = INA226(busnum=1, address=0x40, max_expected_amps=100, shunt_ohms=0.00075, log_level=logging.INFO)
	INA226_Pv2     = INA226(busnum=1, address=0x41, max_expected_amps=100, shunt_ohms=0.00075, log_level=logging.INFO)

	INA226s = (
		INA226_Battery,
		INA226_Pv1,
		INA226_Pv2,
	)

	for ina226 in INA226s:
		if ina226 is not None:
			ina226.configure()

	while(1):
		if INA226_Battery is not None:
			bat_v = INA226_Battery.voltage()
			bat_a = INA226_Battery.current() / 1000.
		else:
			bat_v = 0
			bat_a = 0

		if INA226_Pv1 is not None:
			pv1_v = INA226_Pv1.voltage()
			pv1_a = INA226_Pv1.current() / 1000.
		else:
			pv1_v = 0
			pv1_a = 0

		if INA226_Pv2 is not None:
			pv2_v = INA226_Pv2.voltage()
			pv2_a = INA226_Pv2.current() / 1000.
		else:
			pv2_v = 0
			pv2_a = 0

		url = BASEURL % ( pv1_v, pv1_a, bat_v, bat_a, pv2_v, pv2_a )
		print(str(datetime.now()) + ' ' +  url, flush=True)

		req = urllib.request.Request(url)
		try:
			with urllib.request.urlopen(req) as res:
				body = res.read()
		except urllib.error.HTTPError as err:
			print(err.code, flush=True)
			sys.exit(10)
		except urllib.error.URLError as err:
			print(err.reason, flush=True)
			sys.exit(20)

		sleep(10)
