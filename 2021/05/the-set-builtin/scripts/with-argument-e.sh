#!/usr/bin/env bash

# https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
# • -e:  Exit immediately if a command exits with a non-zero status.
set -e

python the_set_builtin/sample_1.py
python the_set_builtin/sample_2_force_error.py
python the_set_builtin/sample_3.py
