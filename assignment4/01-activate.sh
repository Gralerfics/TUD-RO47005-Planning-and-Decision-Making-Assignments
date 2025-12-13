#!/usr/bin/env bash

# this file is meant to be sourced by bash to set environment
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This file is meant to be sourced. Please run"
    echo "source $0"
    exit 1
fi

# set variable to announce that we're properly sourced (to be checked in successive scripts)
export PDM_SOURCED=

# absolute path of this script file
THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
# use 'source' for TA's (they have the 'source' dir) or 'release' (for students)
if [ -d "${THIS_DIR}/source" ]; then
    export SOURCE_DIR="${THIS_DIR}/source"
elif [ -d "${THIS_DIR}/release" ]; then
    export SOURCE_DIR="${THIS_DIR}/release"
fi


source $THIS_DIR/miniforge3/bin/activate

echo
echo "Adding $SOURCE_DIR to PYTHONPATH"
export PYTHONPATH="$SOURCE_DIR:$PYTHONPATH"

# activate conda environment pdm4
conda activate pdm4
