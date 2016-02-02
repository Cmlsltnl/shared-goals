#!/bin/sh
. /home/maarten/code/shared_goals/env/bin/activate

case $1 in
    start)
        PYTHONPATH="/home/maarten/code/shared_goals/src/" watchmedo shell-command --patterns="*_html.py" --recursive --command='python ${watch_src_path} > `echo "${watch_src_path}" | sed s/_html.py/.html/`' /home/maarten/code/shared_goals/src/ &
        echo $! > /home/maarten/code/shared_goals/bin/update_html.pid
        ;;
    stop)
       kill `cat /home/maarten/code/shared_goals/bin/update_html.pid`
       rm /home/maarten/code/shared_goals/bin/update_html.pid
       ;;
     *)
       echo "usage: update_html {start|stop}" ;;
esac
