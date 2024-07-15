#!/bin/bash

pip install --upgrade pip
pip install poetry

poetry config virtualenvs.in-project true

git config --global --add safe.directory /workspaces/AIGA

make setup
