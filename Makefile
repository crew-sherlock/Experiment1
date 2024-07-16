PYV=$(shell python -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)");

setup:
	poetry env use python3.9
	poetry config virtualenvs.in-project true
	poetry install --with dev
	poetry run pre-commit install

pre-commit:
	poetry run pre-commit run --all-files

serve-docs:
	poetry run mkdocs serve

build-docs:
	poetry run mkdocs build

requirements:
	@find promptflow -name 'requirements.txt' -execdir poetry export --without-hashes -o {} \;

clean:
	rm -rf site

ci-build: lint unittest

lint:
	@echo -e "\e[34m$@\e[0m" || true
	@poetry run flake8 src

unittest:
	@echo -e "\e[34m$@\e[0m" || true
	@poetry run pytest -vvv
