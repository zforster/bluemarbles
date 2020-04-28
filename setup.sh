#!/bin/bash

python3 -m venv venv

./venv/bin/activate

python setup.py install

python3 main.py