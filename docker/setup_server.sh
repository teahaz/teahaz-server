#!/bin/bash

# this is not a working file, just a bunch of commands that I will need to make a working file
# most of this app should be integrated with deploy.sh
# also the container should crash if anything in that file crashesj
gunicorn --bind 0.0.0.0:13337 main:app



# server {
#     listen 80;
#     server_name 192.168.1.78;
#
#     location / {
#         include proxy_params;
#         proxy_pass http://localhost:13337;
#     }
# }
