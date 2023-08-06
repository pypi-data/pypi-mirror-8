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

host=${1:-"localhost"}
port=${2:-2222}

python ./manager.py runserver -h${host} -p${port} -r -d
