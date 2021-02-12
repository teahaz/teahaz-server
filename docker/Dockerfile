# WARNING: this dockerfile is not complete and cannot be used to run the server yet
################################################################################################
#Dockerfile for running the server easier
# build with:
#   sudo docker build -t teahaz_server:latest .
#
# run server:
#   sudo docker run --rm -v $pwd/server/:/server teahaz_server:latest
#
#stop server:
#   sudo docker kill <container id>
#
# get shell with: [NOTE the server has to be running for this]
#   sudo docker exec -it <container id> /bin/bash
################################################################################################

#docker run -it -v /Users/bdbot/Documents/mount_demo/:/mount_demo nycdsa/linux-toolkits bash
#sudo docker run -v $pwd:/server teahaz_server:latest

FROM ubuntu:20.04
RUN apt-get update && apt-get upgrade -y





# install stuff
RUN apt install git -y
RUN apt install cron -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install python3-wheel -y

RUN pip3 install flask
RUN pip3 install flask_restful

RUN pip3 install uuid
RUN pip3 install bcrypt




# setup
EXPOSE 13337
RUN useradd -m teahaz

RUN mkdir /server
RUN chown teahaz /server
RUN chmod -R u+wrx /server

RUN su teahaz # dont want it to have a password so there is no chance of gettitng root back

WORKDIR /server

CMD cd /server/docker; ./deploy.sh
