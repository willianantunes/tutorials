#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -eu -o pipefail

CSPROJ_PATH=./src

./scripts/generate-migrations.sh
./scripts/apply-migrations.sh

echo "### Running and watching the project 👀"
# If you'd like to check all commands available: dotnet watch --project ./src run -- --help
dotnet watch --project $CSPROJ_PATH run -- api
