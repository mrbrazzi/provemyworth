#!/usr/bin/env bash
set -e
shopt -s extglob globstar

source $VENV_HOME/bin/activate
cd $SRC_HOME
python pyw.py
#python -m cProfile -s cumtime pyw.py

exec "$@"