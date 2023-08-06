#!/usr/bin/env bash
source $(dirname $0)/scripts/env_conf.sh
root=$(dirname $(${abspath} $0)) 2>/dev/null
root=${root:-.}
cd ${root}

# dev
export PY_BIN_DIR=${root}/venv/bin
source ${PY_BIN_DIR}/activate
export SYSTEM_CONFIG=development

# prod
# export PY_BIN_DIR=/usr/local/venvs/$(PROJECT_NAME)s/bin
# source ${PY_BIN_DIR}/activate
# export SYSTEM_CONFIG=production
