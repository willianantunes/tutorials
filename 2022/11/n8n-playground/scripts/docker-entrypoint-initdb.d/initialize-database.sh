#!/bin/bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

echo "Your environments..."
DATABASE_PRD=db_tmp
APP_SCHEMA_PRD=tmp_schema_prd
APP_ROLE_PRD=role_tmp_prd
APP_DEFAULT_PASSWORD=please-dont-use-this-password-ever

echo "###### Creating environment"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE DATABASE "$DATABASE_PRD";
  \c "$DATABASE_PRD";
  CREATE SCHEMA IF NOT EXISTS "$APP_SCHEMA_PRD";
  CREATE ROLE "$APP_ROLE_PRD" WITH LOGIN CREATEDB PASSWORD '$APP_DEFAULT_PASSWORD';
  GRANT ALL PRIVILEGES ON SCHEMA "$APP_SCHEMA_PRD" TO "$APP_ROLE_PRD";
  ALTER ROLE "$APP_ROLE_PRD" IN DATABASE "$DATABASE_PRD" SET search_path TO $APP_SCHEMA_PRD;
EOSQL

echo "###### Creating tables for $DATABASE_PRD/$APP_SCHEMA_PRD"
psql -v ON_ERROR_STOP=1 --username "$APP_ROLE_PRD" --dbname "$DATABASE_PRD" <<-EOSQL
  CREATE TABLE IF NOT EXISTS "tmp_random_table"
  (
      "id"             INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
      "created_at"     TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
      "correlation_id" VARCHAR(36)  NOT NULL,
      "message"        VARCHAR(128) NOT NULL,
      "metadata"       JSONB NULL,
      CONSTRAINT unique_correlation UNIQUE (correlation_id)
  );
EOSQL
