export PYTHONPATH=$PYTHONPATH:$(pwd)/..
DEBUG="--debug"
[[ $1 = prod ]] && DEBUG=""
flask run ${DEBUG} -p 5001
