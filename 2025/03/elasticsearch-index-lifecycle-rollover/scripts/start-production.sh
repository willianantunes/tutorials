#!/usr/bin/env bash

# https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
# -e  Exit immediately if a command exits with a non-zero status.
# -x Print commands and their arguments as they are executed.
set -e

python manage.py
