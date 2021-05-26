#!/usr/bin/env bash

if [ -z "$1" ]; then
  echo "Please provide your project name as an argument 👀, such as: $0 YourProjectName"
  exit 0
fi

echo "### Reading variables..."
PROJECT_BUSINESS_NAME=$1
PROJECT_TESTS_NAME=Tests

# You can use the command "dotnet new -l" in order to list all templates available.
# In this script we are using: sln, webapi and xunit templates!

echo "### Solution setup!"
dotnet new sln -n $PROJECT_BUSINESS_NAME
# Then two projects:
# - One which contains all the business and infrastructure code
# - Another that is focused on tests only
echo "### Creating projects $PROJECT_BUSINESS_NAME and $PROJECT_TESTS_NAME"
dotnet new webapi -o $PROJECT_BUSINESS_NAME -n $PROJECT_BUSINESS_NAME --no-https
dotnet new xunit -o tests -n $PROJECT_TESTS_NAME
echo "### Adding them to the solution..."
# Finally we add them to our solution
dotnet sln add $PROJECT_BUSINESS_NAME
dotnet sln add tests
echo "### Don't forget to configure InvariantGlobalization, Nullable and so forth in your production-ready project!"
echo "### Done! You're good to go 😍"
