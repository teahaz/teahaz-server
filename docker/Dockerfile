FROM ubuntu:20.04


# arguments
ARG TEAHAZ_PORT=13337


# environment variables
ENV PYTHONUNBUFFERED=0
ENV DEBIAN_FRONTEND=noninteractive
ENV TEAHAZ_PORT=${TEAHAZ_PORT}


# install and update system stuff
RUN apt-get update && apt-get upgrade -y
RUN apt install apt-utils -y
RUN apt install systemctl -y


# install general things
RUN apt install git -y
RUN apt install cron -y
RUN apt install psmisc -y
RUN apt install busybox -y


# install for flask server
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install python3-wheel -y

RUN pip3 install flask
RUN pip3 install flask_restful
RUN pip3 install uuid
RUN pip3 install bcrypt


# install for prod environment
RUN apt install nginx -y
RUN pip3 install gunicorn


# setup stuff for prod environment
EXPOSE 80
EXPOSE 443
COPY nginx_config /etc/nginx/sites-enabled/default
COPY /etc/letsencrypt/live/teahaz.co.uk/ /etc/letsencrypt/live/teahaz.co.uk/


# setup permissions
RUN useradd -m teahaz
RUN chown teahaz /home/teahaz
RUN chgrp teahaz /home/teahaz
RUN chmod -R u+wrx /home/teahaz
RUN chmod -R g+wrx /home/teahaz

# RUN chmod -R a+x /home/teahaz/docker/deploy.sh
# RUN chmod -R a+x /home/teahaz/docker/update.sh
# RUN chmod -R a+x /home/teahaz/docker/root_deploy.sh



# set user and work dir
# USER teahaz
WORKDIR /home/teahaz



# run
CMD cd /home/teahaz/docker/; ./deploy.sh











################################
# working on stuff
# ENV TEAHAZ_PORT=13337
# EXPOSE 80
#
# RUN apt install ngnix
# RUN pip3 install gunicorn
#
# # cron start nginx
#
# RUN rm /etc/nginx/sites-enabled/default 

# copy docker/nginx_config to /etc/nginx/sites-enabled/teahaz
# the last part of that is the new name of nginx_config



################################


