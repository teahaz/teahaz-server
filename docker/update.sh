while [ 1 ];
do
    git pull

    if [ "$?" != 0 ]
    then
        # pull failed
       echo "\e[0;31m==========================="
       echo "error pulling new changes"
       echo "===========================\e[0;37m"

        # oneliner uses the python logging function to create a log of git failing
        cd ../server/; python -c "import logging_th as log;log.logger(level='warning', msg='failed to pull updates from git')";cd ../docker
    fi

    sleep 60
done

