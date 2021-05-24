
# just standard run
run:
	sudo docker-compose up


# rebuild the image
rebuild:
	sudo docker-compose build --no-cache
	sudo docker-compose up


# update the image
update:
	git pull --force
	sudo docker-compose build --no-cache

# resets/creates config files
setup:
	cp ./healthcheck/templates/on_error.py ./healthcheck/
	cp ./healthcheck/templates/settings.json ./healthcheck/
