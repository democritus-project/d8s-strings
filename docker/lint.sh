#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort democritus_strings/ tests/

black democritus_strings/ tests/

mypy democritus_strings/ tests/

pylint --fail-under 9 democritus_strings/*.py

flake8 democritus_strings/ tests/

bandit -r democritus_strings/

# we run black again at the end to undo any odd changes made by any of the linters above
black democritus_strings/ tests/
