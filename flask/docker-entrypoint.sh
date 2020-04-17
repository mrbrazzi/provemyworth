#!/usr/bin/env bash
set -e
shopt -s extglob globstar

source $VENV_HOME/bin/activate
cd $SRC_HOME
export FLASK_APP=pyw.py
python -m flask run --host=0.0.0.0

exec "$@"