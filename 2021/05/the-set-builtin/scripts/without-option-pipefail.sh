#!/usr/bin/env bash

# https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
# • -e:  Exit immediately if a command exits with a non-zero status.
set -e

this-is-a-fake-command-my-friend | echo "You...are late."
echo "A thousand apologies, O patient one."
