# WARNING: this dockerfile is not complete and cannot be used to run the server yet
################################################################################################
#Dockerfile for running the server easier
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
FROM ubuntu:20.04

# installs
# apt 
RUN apt-get update && apt-get upgrade -y
RUN apt install python3  python3-pip python3-wheel -y

#run apt install vim -y #pls dont edit files in the container as they will be owned by root 
RUN apt install nano -y # installing nano so there will be no insentive to edit inside the docker container

#pip
RUN pip3 install flask flask_restful file_read_backwards


#other 
RUN mkdir /server
WORKDIR /server 


#drop privilages
# this i will leave out for testing, but needs to be added for prod
# create a user who has no acces to root or sudo, and switch everything to that user after everyting else is done


CMD cd /server; python3 server.py
