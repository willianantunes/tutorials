#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -eu -o pipefail

PROJECT_NAME=CSharpWebAPIHowToEndpointIT
CSPROJ_PATH=./$PROJECT_NAME

echo "### Running and watching the project 👀"
dotnet watch --project $CSPROJ_PATH run --urls $ASPNETCORE_URLS
