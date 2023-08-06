#!/usr/bin/env bash
#set -x
#set -e
source $(dirname $0)/scripts/env_conf.sh
root=$(dirname $(${abspath} $0))
cd ${root}

if ! source ./env.local.sh; then
    echo "${root}/env.local.sh not exists." >/dev/stderr
    echo "need local env config." >/dev/stderr
    exit 123
fi

if [ $# -lt 2 ]; then
    echo "usage: $0 host port" >/dev/stderr
    exit 123
fi
host=$1
port=$2

exec ${PY_BIN_DIR}/gunicorn -c ${root}/deploy/gunicorn.conf -b$host:$port -w7 -kgevent wsgi:app
