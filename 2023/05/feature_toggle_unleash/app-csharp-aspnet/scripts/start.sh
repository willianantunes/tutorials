#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

dotnet run --project commands seed

dotnet watch --project src -- run --urls $ASPNETCORE_URLS