#!/bin/bash

echo "Creating Python Virtual Env"

python3 -m venv venv

echo "Created Python Virtual Env"

echo "Activating Python Virtual Env"

source ./venv/bin/activate

echo "Activated Python Virtual Env"

echo "Installing Packages"

pip install noise==1.2.2
pip install pycairo==1.19.1

echo "Generating World"

python3 main.py

echo "Done!"