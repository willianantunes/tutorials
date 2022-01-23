#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -eu -o pipefail

COVER_PROJECT_PATH=.
TESTS_PROJECT_PATH=tests

# PYTHONPATH is needed if you use a plugin.
# Let's say you include addopts in pytest.ini with the following: -p tests.support.my_honest_plugin
PYTHONPATH=. pytest $TESTS_PROJECT_PATH -vv
