#!/usr/bin/env python3

# https://github.com/e71828/pi_ina226

import logging
from ina226 import INA226
from time import sleep
import urllib.request
from datetime import datetime

BASEURL = "https://iot.344.jp/put_multi.cgi?DEV=BTPV1&VAL=%.2f,%.2f,%.2f,%.2f"

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

def read(ina):
	V = ina.voltage()
	A = ina.current() / 1000.
	W = ina.power() / 1000.

	#print("%.2fV %.2fA %.2fW" % (V, A, W))


if __name__ == "__main__":
	INAs = (
		None, # INA226(busnum=1, address=0x40, max_expected_amps=100, shunt_ohms=0.00075, log_level=logging.INFO),
		INA226(busnum=1, address=0x44, max_expected_amps=100, shunt_ohms=0.00075, log_level=logging.INFO),
	)

	for ina in INAs:
		if ina is not None:
			ina.configure()

	while(1):
		if INAs[0] is not None:
			v1 = INAs[0].voltage()
			a1 = INAs[0].current() / 1000.
		else:
			v1 = 0
			a1 = 0

		if INAs[1] is not None:
			v2 = INAs[1].voltage()
			a2 = INAs[1].current() / 1000.
		else:
			v2 = 0
			a2 = 0

		url = BASEURL % ( v1, a1, v2, a2 )
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
