#!/bin/bash

echo "Creating Python Virtual Env"

python3 -m venv venv

echo "Created Python Virtual Env"

echo "Activating Python Virtual Env"

source ./venv/bin/activate

echo "Activated Python Virtual Env"

echo "Installing Packages"

python setup.py install

python3 main.py