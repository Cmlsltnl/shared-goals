#!/bin/sh
. /home/maarten/code/shared_goals/env/bin/activate

case $1 in
    start)
        2>&1 python /home/maarten/code/shared_goals/src/manage.py runserver 1>/home/maarten/code/shared_goals/bin/log/django_server.log &
        echo $! > /home/maarten/code/shared_goals/bin/django_server.pid
        ;;
    stop)
       kill `cat /home/maarten/code/shared_goals/bin/django_server.pid`
       rm /home/maarten/code/shared_goals/bin/django_server.pid
       ;;
     *)
       echo "usage: django_server {start|stop}" ;;
esac
