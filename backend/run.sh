#!/bin/sh -x
BASE=$(dirname ${0})
export BACKEND_ENV="${BASE}/sample.env"
export LOG_PATH=${BASE}/logs
LISTENING_PORT=$(grep -i '^LISTENING_PORT' $BACKEND_ENV | sed 's/^[^=]* *= *//g' | tr -d '"')
LISTENING_HOST=$(grep -i '^LISTENING_HOST' $BACKEND_ENV | sed 's/^[^=]* *= *//g' | tr -d '"')
mkdir -p $LOG_PATH
uvicorn --env-file $BACKEND_ENV --port $LISTENING_PORT --app-dir ${BASE} --host $LISTENING_HOST --reload main:app
