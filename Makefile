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

