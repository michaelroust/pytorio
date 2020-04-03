#!/usr/bin/env bash

echo 'Setup Script Started ...'
python3 -m venv env
source env/bin/activate
echo 'Installing requirements to venv'
pip install -r requirements.txt
echo 'Done!'
