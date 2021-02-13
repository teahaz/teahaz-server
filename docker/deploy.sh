DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo "----------------------------------------------------------------"
echo $DIR
echo "----------------------------------------------------------------"

cd $DIR

./update.sh &

cd $DIR/../server

python3 main.py
