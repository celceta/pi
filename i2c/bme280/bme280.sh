#!/bin/sh

ADDRESS=0x76

case "$1" in
	"config")
		i2cset -y 1 $ADDRESS 0xf5 0x80 i; echo $?
		i2cset -y 1 $ADDRESS 0xf4 0x27 i; echo $?
		i2cset -y 1 $ADDRESS 0xf2 0x00 i; echo $?
		;;
	"get")
		hum_lsb=`i2cget -y 1 $ADDRESS 0xfe`
		hum_msb=`i2cget -y 1 $ADDRESS 0xfd`
		temp_xlsb=`i2cget -y 1 $ADDRESS 0xfc`
		temp_lsb=`i2cget -y 1 $ADDRESS 0xfb`
		temp_msb=`i2cget -y 1 $ADDRESS 0xfa`
		press_xlsb=`i2cget -y 1 $ADDRESS 0xf9`
		press_lsb=`i2cget -y 1 $ADDRESS 0xf8`
		press_msb=`i2cget -y 1 $ADDRESS 0xf7`

		humidity=`echo ${hum_msb}${hum_lsb} | tr -d '0x'`
		temperature=`echo ${temp_msb}${temp_lsb}${temp_xlsb} | tr -d '0x'`
		pressure=`echo ${press_msb}${press_lsb}${press_xlsb} | tr -d '0x'`

		echo $humidity
		echo $temperature
		echo $pressure

		humidity=`hex2dec $humidity`
		temperature=`hex2dec $temperature`
		pressure=`hex2dec $pressure`


		echo $humidity
		echo $temperature
		echo $pressure
		;;
	"reset")
		i2cset -y 1 $ADDRESS 0xe0 0x00; echo $?
		;;
esac

