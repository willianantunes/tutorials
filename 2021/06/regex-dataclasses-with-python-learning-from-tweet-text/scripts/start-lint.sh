#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -eu -o pipefail

TARGET_PROJECT=regex_dataclasses
TARGET_TEST_PROJECT=tests
TARGET_FOLDERS="$TARGET_PROJECT $TARGET_TEST_PROJECT"

echo "######## ISORT..."
isort $TARGET_FOLDERS --check-only --diff
echo "######## BLACK..."
black --check --diff $TARGET_FOLDERS
echo "######## MYPY..."
# mypy will only target the project folder
mypy $TARGET_PROJECT
