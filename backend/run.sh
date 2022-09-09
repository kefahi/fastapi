#!/bin/sh

# Python: use ipdb instead of pdb
export PYTHONBREAKPOINT=ipdb.set_trace

BASEDIR=$(dirname "$(realpath $0)")
export BACKEND_ENV="${BACKEND_ENV:-${BASEDIR}/secrets.env}"
LISTENING_PORT=$(grep -i '^LISTENING_PORT' $BACKEND_ENV | sed 's/^[^=]* *= *//g' | tr -d '"' | tr -d "'")
LISTENING_HOST=$(grep -i '^LISTENING_HOST' $BACKEND_ENV | sed 's/^[^=]* *= *//g' | tr -d '"' | tr -d "'")

cd $BASEDIR
hypercorn --log-config json_log.ini -w 1 --backlog 200 -b $LISTENING_HOST':'$LISTENING_PORT -k 'asyncio' main:app
