setup:
	poetry install --with dev
	poetry run pre-commit install

pre-commit:
	poetry run pre-commit run --all-files

build-docs:
	poetry run mkdocs build

clean:
	rm -rf site

