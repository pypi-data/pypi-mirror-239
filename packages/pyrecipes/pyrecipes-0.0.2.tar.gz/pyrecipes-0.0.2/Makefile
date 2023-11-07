.PHONY = lint test

default: lint test

lint:
	flake8 pyrecipes tests

test:
	pytest tests

coverage:
	coverage run --source pyrecipes -m pytest tests; coverage report

pip-install:
	pip install pip-tools
	pip-compile
	pip-sync
