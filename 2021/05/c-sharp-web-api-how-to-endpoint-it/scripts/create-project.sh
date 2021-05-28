#!/usr/bin/env bash

if [ -z "$1" ]; then
  echo "Please provide your project name as an argument 👀, such as: $0 YourProjectName"
  exit 0
fi

echo "### Reading variables..."
PROJECT_BUSINESS_NAME=$1
PROJECT_BUSINESS_PATH=src
PROJECT_TESTS_NAME=Tests
PROJECT_TESTS_PATH=tests

# You can use the command "dotnet new -l" in order to list all templates available.
# In this script we are using: sln, webapi and xunit templates!

echo "### Solution setup!"
# Within the solution we'll have two projects:
# - One which contains all the business and infrastructure code
# - Another that is focused on tests only
dotnet new sln -n $PROJECT_BUSINESS_NAME

echo "### Creating projects $PROJECT_BUSINESS_NAME and $PROJECT_TESTS_NAME"
dotnet new webapi -o $PROJECT_BUSINESS_PATH -n $PROJECT_BUSINESS_NAME --no-https
dotnet new xunit -o $PROJECT_TESTS_PATH -n $PROJECT_TESTS_NAME

echo "### Adding them to the solution..."
dotnet sln add $PROJECT_BUSINESS_PATH

echo "### Creating references and cleaning up..."
dotnet add $PROJECT_TESTS_PATH reference $PROJECT_BUSINESS_PATH
dotnet clean

echo "### Don't forget to configure InvariantGlobalization, Nullable and so forth in your production-ready project!"
echo "### Done! You're good to go 😍"
