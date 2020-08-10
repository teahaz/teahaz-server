# the porpuse of this dockerfile isnt for testing, it is for rolling out, it should handle automatic updates and some basic condom like security + whatever else server might need
###################################################################################################
#Dockerfile for running the server easier
# build with:
#   sudo docker build -t teahaz_server:latest .
#
# run server:
#   sudo docker run --rm -v $PWD:/server teahaz_server:latest
#
# get shell with: [you reall shouldnt need this tho]
#   sudo docker run --rm -ti -v $PWD:/server teahaz_server:latest
###################################################################################################
from ubuntu:20.04

# installs
# apt 
run apt-get update && apt-get upgrade -y
run apt install python3  python3-pip python3-wheel -y

#run apt install vim -y #pls dont edit files in the container as they will be owned by root 
run apt install nano -y # installing nano so there will be no insentive to edit inside the docker container

#pip
run pip3 install flask    


#other 
run mkdir /server
workdir /server

run python3 server.py
