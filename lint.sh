#!/bin/sh

flake8 tests src setup.py
pylint --rcfile=pylint.rc src/django_livefield
pylint --rcfile=pylint.rc tests
pylint --rcfile=pylint.rc setup.py
