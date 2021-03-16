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


runc systemctl enable cron
runc systemctl start cron

runc systemctl enable nginx
runc nginx -t
runc systemctl start nginx

# add changing permissions to cron, so it auto-fixes itself if someone git pulls as root
# not sure why this doesnt work with runc, but it should be fine like this
(crontab -l 2>/dev/null; echo "* * * * * chown -R teahaz /home/teahaz") | crontab -

