while [ 1 ];
do
    git pull

    if [ "$?" != 0 ]
    then
       echo "\e[0;31m==========================="
       echo "error pulling new changes\n"
       echo "===========================\e[0;37m"
    fi

    sleep 60
done

