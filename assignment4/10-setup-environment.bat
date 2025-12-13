@echo off
call conda env create -f environment.yml
call 01-activate.bat
call pip install -r requirements.txt