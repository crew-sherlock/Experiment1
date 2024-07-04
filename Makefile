setup:
	poetry install --with dev
	poetry run pre-commit install

pre-commit:
	poetry run pre-commit run --all-files

serve-docs:
	poetry run mkdocs serve

build-docs:
	poetry run mkdocs build

clean:
	rm -rf site

ci-build: lint unittest

lint:
	@echo -e "\e[34m$@\e[0m" || true
	@poetry run flake8 src

unittest:
	@echo -e "\e[34m$@\e[0m" || true
	@poetry run pytest -vvv