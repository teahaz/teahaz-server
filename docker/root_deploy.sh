#!/bin/bash
id | grep "uid=0" > /dev/null
if [ "$?" != 0 ]
then
    echo "ERR: script needs to be run as root"
    exit
fi


function runc() {
    echo "root_script running: $@"
    $@
    if [ "$?" != 0 ]
    then
        killall python3
    fi
}

runc systemctl enable nginx
runc nginx -t
runc systemctl start nginx

