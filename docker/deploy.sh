./update.sh &

cd ../server

# python3 -u main.py
gunicorn --bind 0.0.0.0:13337 --log-level=debug main:app

