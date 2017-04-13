#!/bin/sh

PATH="$PATH:/usr/bin/sh"

sw=0
current=0
prev=0

i2c_tsl2561.py init

while true
do
	current=`i2c_tsl2561.py get`
	#echo $current

	if [ $sw -eq 0 ]; then
		# in-off
		if [ `echo "$prev >= 0.05 && $current >= 0.05" | bc` = 1 ]; then
			echo "`date` : turn ON"
			i2c_SeeedRelay.py 1 1
			sw=1
		fi
	else
		# in-on
		if [ `echo "$prev < 0.05 && $current < 0.05" | bc` = 1 ]; then
			echo "`date` : turn OFF"
			i2c_SeeedRelay.py 1 0
			sw=0
		fi
	fi

	prev=$current

	sleep 1
done


