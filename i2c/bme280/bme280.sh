#!/bin/sh

ADDRESS=0x76

case "$1" in
	"config")
		i2cset -y 1 $ADDRESS 0xf5 0xA0 i # config    101(1000ms) 000(filter off) 0 0(spi off)
		i2cset -y 1 $ADDRESS 0xf4 0x27 i # ctrl_meas 001(x1) 001(x1) 11(normal mode)
		i2cset -y 1 $ADDRESS 0xf2 0x01 i # ctrl_hum  001(x1)
		;;
	"get")
		hum_lsb=00`   i2cget -y 1 $ADDRESS 0xfe | tr -d '0x'`
		hum_msb=00`   i2cget -y 1 $ADDRESS 0xfd | tr -d '0x'`
		temp_xlsb=00` i2cget -y 1 $ADDRESS 0xfc | tr -d '0x'`
		temp_lsb=00`  i2cget -y 1 $ADDRESS 0xfb | tr -d '0x'`
		temp_msb=00`  i2cget -y 1 $ADDRESS 0xfa | tr -d '0x'`
		press_xlsb=00`i2cget -y 1 $ADDRESS 0xf9 | tr -d '0x'`
		press_lsb=00` i2cget -y 1 $ADDRESS 0xf8 | tr -d '0x'`
		press_msb=00` i2cget -y 1 $ADDRESS 0xf7 | tr -d '0x'`

		humidity=`expr $hum_msb : '.*\(..\)$'``expr $hum_lsb : '.*\(..\)$'`
		temperature=`expr $temp_msb : '.*\(..\)$'``expr $temp_lsb : '.*\(..\)$'``expr $temp_xlsb : '.*\(..\)$'`
		pressure=`expr $press_msb : '.*\(..\)$'``expr $press_lsb : '.*\(..\)$'``expr $press_xlsb : '.*\(..\)$'`

		#echo $humidity
		#echo $temperature
		#echo $pressure

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

