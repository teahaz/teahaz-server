DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR

./update.sh &

cd $DIR/../server

python3 -u main.py
