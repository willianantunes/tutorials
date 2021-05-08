#!/usr/bin/env bash

# https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
# • -e:  Exit immediately if a command exits with a non-zero status.
# • pipefail: Return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status,
# or zero if all commands in the pipeline exit successfully. This option is disabled by default.
set -e -o pipefail

this-is-a-fake-command-my-friend | echo "You...are late."
echo "A thousand apologies, O patient one."

