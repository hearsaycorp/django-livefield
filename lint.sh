#!/usr/bin/env sh

flake8 tests src setup.py
if [ $? -ne 0 ]; then
    echo "Flake8 linting failed."
    exit 1
fi

pylint --rcfile=pylint.rc src/livefield
if [ $? -ne 0 ]; then
    echo "PyLint found errors in src/."
    exit 1
fi

# FIXME: pylint-django doesn't support Django 1.7.
if [ "$DJANGO_VERSION_CEILING" != "1.8" ]; then
    pylint --rcfile=pylint.rc tests
    if [ $? -ne 0 ]; then
        echo "PyLint found errors in test/."
        exit 1
    fi
fi

pylint --rcfile=pylint.rc setup.py
if [ $? -ne 0 ]; then
    echo "PyLint found errors in setup.py."
    exit 1
fi
