#!/usr/bin/env bash
# install required conda packages into conda environment pdm
mamba env create -f environment.yml
# Activate the environment
source ./01-activate.sh
# you can verify with conda env list
pip install -r requirements.txt
