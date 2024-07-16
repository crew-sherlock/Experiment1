#!/bin/bash

pip install --upgrade pip
pip install poetry
pip install poetry-plugin-export

git config --global --add safe.directory /workspaces/AIGA

make setup
