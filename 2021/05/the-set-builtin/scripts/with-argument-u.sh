#!/usr/bin/env bash

# https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
# • -u: Treat unset variables as an error when substituting.
set -u

python the_set_builtin/sample_1.py
python the_set_builtin/sample_2_force_error.py
python the_set_builtin/sample_3.py
python the_set_builtin/sample_4_env_variable.py "$ALADDIN_WISH"
python the_set_builtin/sample_5.py
