#!/bin/bash

sudo apt update && sudo apt upgrade -y

sudo apt install -y python3.12 python3.12-venv

if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

python3 -u main.py
