#while [ 1 ];
#do
#    git pull
#
#    if [ "$?" != 0 ]
#    then
#        echo "error pulling new changes\n"
#        killall python3
#        shutdown now
#        exit
#    fi
#
#    sleep 60
#done
#
