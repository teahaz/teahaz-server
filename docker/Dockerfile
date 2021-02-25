# install and update
FROM ubuntu:20.04
RUN apt-get update && apt-get upgrade -y
RUN apt install apt-utils -y


# evn
ENV PYTHONUNBUFFERED=0
ENV DEBIAN_FRONTEND=noninteractive 



# install stuff
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




# setup
EXPOSE 13337

RUN (crontab -l 2>/dev/null; echo "* * * * * chown -R teahaz /home/teahaz") | crontab -

RUN useradd -m teahaz
RUN chown teahaz /home/teahaz
RUN chgrp teahaz /home/teahaz
RUN chmod -R u+wrx /home/teahaz
RUN chmod -R g+wrx /home/teahaz

USER teahaz
WORKDIR /home/teahaz


# run
CMD cd /home/teahaz/docker/; ./deploy.sh
