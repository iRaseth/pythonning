# Use uv (https://github.com/astral-sh/uv)
UV = uv
PYTHON = python

# Default virtual environment directory
VENV = .venv

# Requirements files
REQ_IN = requirements/app.in
REQ_LOCK = requirements/app.txt

.PHONY: install compile update sync run clean

compile:
	$(UV) pip compile $(REQ_IN) -o $(REQ_LOCK)

install:
	$(UV) pip install -r $(REQ_LOCK)

setup-uv:
	pip install uv

setup-lint:
	pre-commit

init: setup-uv install setup-lint
	echo "Creating everything, for you, my little boy..."
