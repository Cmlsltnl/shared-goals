#!/bin/bash

thisdir=$(dirname $0)
name=`basename $1`
name=${name%.sh}

case $2 in
    start)
       echo $$ > $thisdir/${name}.pid
       source env/bin/activate
       exec 2>&1 $1 1>$thisdir/log/${name}.stdout
       ;;
     stop)
       kill `cat $thisdir/${name}.pid`
       rm $thisdir/${name}.pid
       ;;
     *)
       echo "usage: <path to app> {start|stop}" ;;
 esac