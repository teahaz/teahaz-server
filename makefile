
# just standard run
run:
	sudo docker-compose up


# rebuild the image
rebuild:
	sudo docker-compose build --no-cache
	# sudo docker-compose up


# update the image
update:
	git pull --force
	sudo docker-compose build --no-cache


# resets/creates config files
setup:
	cp ./healthcheck/templates/on_error.py ./healthcheck/
	cp ./healthcheck/templates/settings.json ./healthcheck/


# Sets up a testing environment so you can develop on teahaz easier
# This environment includes running a mongodb docker container and
# 	an instance of teahaz and teapass locally in debug mode.
dev:
	sudo -l # blocking, make sure the password is in sudo cache
	# kill stuff if they are already running
	sudo docker ps | grep  -o "...............mongo"| grep -o "^..............." | sudo xargs -I {} sh -c "docker kill {}" 2> /dev/null # kill mongodb
	ps aux | grep -o ".*python3.*storageServer/src/main.py" | grep -v grep | awk '{print $$2}'| xargs -I{} kill -9 {}
	ps aux | grep -o ".*python3.*teahouse/src/main.py" | grep -v grep | awk '{print $$2}'| xargs -I{} kill -9 {}
	# start everything
	cd ./storage; sudo docker run -p 27017:27017 -v database:/data/db  mongo:latest &
	sleep 2
	echo "You must add '127.0.0.1	mongodb' to /etc/hosts for this dev environment to work!"
	# curl mongodb:27017
	mongo-express 2> /dev/null &
	cd ./storageServer/src/; python3 main.py &
	sleep 1
	cd ./teahouse/src/; python3 main.py
	# kill stuff if teahouse exits
	# sudo docker ps | grep  -o "...............mongo"| grep -o "^..............." | sudo xargs -I {} sh -c "docker kill {}" # kill mongodb
	ps aux | grep -o ".*python3.*storageServer/src/main.py" | grep -v grep | awk '{print $$2}'| xargs -I{} kill -9 {}
	ps aux | grep -o ".*python3.*teahouse/src/main.py" | grep -v grep | awk '{print $$2}'| xargs -I{} kill -9 {}


# .INTERMEDIATE:
# 	sudo docker ps | grep  -o "...............mongo"| grep -o "^..............." | sudo xargs -I {} sh -c "docker kill {}" # kill mongodb
# 	ps aux | grep -o ".*python3.*storageServer/src/main.py" | grep -v grep | awk '{print $$2}'| xargs -I{} kill -9 {}
# 	ps aux | grep -o ".*python3.*teahouse/src/main.py" | grep -v grep | awk '{print $$2}'| xargs -I{} kill -9 {}
