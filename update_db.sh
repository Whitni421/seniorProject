#!/bin/bash

source ./my_venv/bin/activate
# Starting out: download all of your data and create your db by running 
# garmindb_cli.py --all --download --import --analyze

# update data
# Incrementally update your db by downloading the latest data and importing it by running 
garmindb_cli.py --all --download --import --analyze --latest

# copy to senior_project directory
cp -r ~/HealthData /mnt/c/Users/whitn/OneDrive/Desktop/seniorProject