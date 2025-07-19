#!/usr/local/bin/bash

# LOG=/home/harusamesoup/www/HOST/iot.344.jp/logs/q.log
# date >> "$LOG"

typeset DEV
typeset VALUE

function error {
	echo 'Status: 405' # Method Not Allowed
	echo 'Content-type: text/plain'
	echo
	echo "$2"
	exit $1
}

### SSL check
[[ "$HTTPS" != on ]] && error $LINENO 'super BAD request'

### Get parameters
for ONE in ${QUERY_STRING//&/ }
do
	set -- ${ONE//=/ }
	case "$1" in
		DEV)	DEV="$2" ;;
		VAL)	VAL="$2" ;;
	esac
done

# echo "DEV=$DEV"
# echo "VAL=$VAL"

[[ -z "$DEV" ]] && error $LINENO 'Invalid args'
[[ -z "$VAL" ]] && error $LINENO 'Invalid args'

VAL="$VAL,default,default,default,default,default,default,default,default,default,default"
VAL=$( echo "$VAL" | cut -d, -f-12 )

### Start http response
echo 'Content-type: text/plain'
echo

date
echo $QUERY_STRING

SQL="insert into harusamesoup_iot.iotlake_multi values ('$DEV',$VAL)"

echo "$SQL"

mysql --defaults-extra-file=.mysql/mysql.conf <<< "$SQL" 2>&1
echo "select count(*) from harusamesoup_iot.iotlake_multi" | mysql --defaults-extra-file=.mysql/mysql.conf

echo "DONE"

exit 0
