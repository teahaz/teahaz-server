FROM ubuntu:20.04



# arguments
ARG TEAHAZ_PORT





# install and update system stuff
RUN apt-get update && apt-get upgrade -y
RUN apt install apt-utils -y
RUN apt install systemctl -y





# install other stuff
RUN apt install git -y
RUN apt install cron -y
RUN apt install busybox -y

RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install python3-wheel -y

RUN pip3 install flask
RUN pip3 install flask_restful

RUN pip3 install uuid
RUN pip3 install bcrypt


# evn
ENV PYTHONUNBUFFERED=0
ENV DEBIAN_FRONTEND=noninteractive
ENV TEAHAZ_PORT=${TEAHAZ_PORT}


# setup
EXPOSE ${TEAHAZ_PORT}

RUN (crontab -l 2>/dev/null; echo "* * * * * chown -R teahaz /home/teahaz") | crontab -
RUN systemctl enable cron
RUN systemctl start cron

RUN useradd -m teahaz
RUN chown teahaz /home/teahaz
RUN chgrp teahaz /home/teahaz
RUN chmod -R u+wrx /home/teahaz
RUN chmod -R g+wrx /home/teahaz

USER teahaz
WORKDIR /home/teahaz


# run
CMD cd /home/teahaz/docker/; ./deploy.sh
