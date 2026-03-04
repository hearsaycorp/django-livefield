REPO = $(shell git rev-parse --show-toplevel)
POETRY = poetry

install-build:
	${POETRY} install --only=main

install-dev:
	${POETRY} install

poetry:
	curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.4 python3 -
	poetry cache clear pypi --all
	poetry config virtualenvs.in-project true

quickstart: poetry install-dev

quickstart-build: poetry install-build

clean:
	# Delete all .pyc and .pyo files.
	find ${REPO} \( -name "*~" -o -name "*.py[co]" -o -name ".#*" -o -name "#*#" \) -exec rm -f '{}' +
	rm -rf build dist src/django_livefield.egg-info django_livefield.egg-info

lint: clean
	${POETRY} run flake8 --config=${REPO}/setup.cfg ${REPO}/src/livefield/ ${REPO}/tests/
	${POETRY} run pylint --rcfile=${REPO}/pylint.rc ${REPO}/src/livefield/ ${REPO}/tests/

test: clean
	${POETRY} run python ${REPO}/tests/run_tests.py

build:
	${POETRY} build
