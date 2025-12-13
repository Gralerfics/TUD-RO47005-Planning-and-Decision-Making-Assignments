#!/usr/bin/env bash
# install required conda packages into conda environment pdm
mamba env create -f environment.yml
# you can verify with conda env list
source ./01-activate.sh
pip install -r requirements.txt
