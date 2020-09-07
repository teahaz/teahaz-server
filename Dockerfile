################################################################################################
#Dockerfile for running the server easier [includes the database for now as well]
# build with:
#   sudo docker build -t teahaz_server:latest .
#
# run server:
#   sudo docker run --rm -v $PWD/server:/server teahaz_server:latest
#
#stop server:
#   sudo docker kill <container id>
#
# get shell with: [NOTE the server has to be running for this]
#   sudo docker exec -it <container id> /bin/bash
################################################################################################
from ubuntu:20.04

# installs
# apt 
run apt-get update && apt-get upgrade -y
run apt install python3  python3-pip python3-wheel -y
run apt install mysql-server -y

#run apt install vim -y #pls dont edit files in the container as they will be owned by root 
run apt install nano -y # installing nano so there will be no insentive to edit inside the docker container

#pip
run pip3 install flask flask_restful file_read_backwards


#other 
run mkdir /server
workdir /server

cmd cd /server
CMD python3 server.py
