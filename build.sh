#!/usr/bin/env sh

# Safer to update these separately.
pip install -U "setuptools"
pip install -U "wheel"
pip install -U "pip"

./setup.py sdist
./setup.py bdist_wheel
