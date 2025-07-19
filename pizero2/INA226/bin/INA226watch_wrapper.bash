#!/bin/bash

function LOG
{
	echo $(date '+%F %T') "$*"
}

LOG 'Waiting: /dev/i2c-1'

until test -e /dev/i2c-1
do
	sleep 1
done

LOG 'Found: /dev/i2c-1'

while true
do
	LOGFILE=/home/tak/logs/INA226watch.$(date '+%Y%m%d_%H%M%S').log

	LOG Start: $LOGFILE
	/home/tak/python/INA226/INA226watch.py > "$LOGFILE" 2>&1
	LOG Done: $? $LOGFILE

	LOG Sleep: 10s
	sleep 10
done
