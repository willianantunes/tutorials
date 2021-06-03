#!/usr/bin/env bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -eu -o pipefail

CSPROJ_PATH=./src

# https://docs.microsoft.com/en-us/ef/core/managing-schemas/migrations/managing?tabs=dotnet-core-cli
# A poor attempt to use a generated name like Django does: https://docs.djangoproject.com/en/3.2/ref/django-admin/#cmdoption-makemigrations-name
# The first one will be 0, followed by 1, 2, 3, and so forth...
MIGRATIONS_DIRECTORY=./src/Migrations
if [[ -d "$MIGRATIONS_DIRECTORY" ]]
then
    MIGRATION_NAME=$(ls -l $MIGRATIONS_DIRECTORY/*.Designer.cs | wc -l)
else
    MIGRATION_NAME=0
fi

echo "### Generating migrations manifests ⏳"
dotnet ef migrations add $MIGRATION_NAME --project $CSPROJ_PATH

echo "### Checking if it was generated previously and deleting it in case 🤔"
SHOULD_DELETE=$(cat $MIGRATIONS_DIRECTORY/*_$MIGRATION_NAME.cs | grep -c "migrationBuilder\." || true)
if (( $SHOULD_DELETE == 0 ))
then
    echo "### Deleting unneeded migration..."
    rm -rf $MIGRATIONS_DIRECTORY/*_$MIGRATION_NAME*.cs
else
    echo "### Everything seems OK 🤟"
fi
