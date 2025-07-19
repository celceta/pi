#!/usr/local/bin/bash

### Start http response
echo 'Content-type: application/json; charset=utf-8'
echo

mysql --defaults-extra-file=.mysql/mysql.conf -s -N -e "select JSON_OBJECT('TIMESTAMP', ts, 'WATT', truncate(value3 * (value4 * 2.0), 0), 'LEVEL', truncate(GetLifePoCapacity(value3), 0)) from harusamesoup_iot.iotlake_multi where dev='BTPV1' order by ts desc limit 1"
