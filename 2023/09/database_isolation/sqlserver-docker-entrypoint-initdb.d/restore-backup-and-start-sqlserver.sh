#!/usr/bin/env bash

echo "------------ Initializing SQL Server..."
/opt/mssql/bin/sqlservr &
sqlservr_pid=$!

check_sqlcmd() {
    /opt/mssql-tools/bin/sqlcmd -U sa -P "$MSSQL_SA_PASSWORD" -Q "SELECT 1" 2>/dev/null
    return $?
}

proceed_if_sqlserver_is_up() {
  max_retries=5
  retry_interval_in_seconds=5
  retry_count=0

  while ! check_sqlcmd; do
      ((retry_count++))

      if [ $retry_count -ge $max_retries ]; then
          echo "------------ Maximum number of retries reached. Exiting."
          exit 1
      fi

      echo "------------ sqlcmd failed. Retrying in $retry_interval_in_seconds seconds (Attempt $retry_count/$max_retries)..."
      sleep $retry_interval_in_seconds
  done
}

proceed_if_sqlserver_is_up

## https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -e

echo "------------ Creating db if does not exist: $DB_DATABASE"
/opt/mssql-tools/bin/sqlcmd -U sa -P $MSSQL_SA_PASSWORD -d master -Q "IF(db_id(N'$DB_DATABASE') IS NULL) CREATE DATABASE $DB_DATABASE;"

echo "------------ Restoring backup..."
/opt/mssql-tools/bin/sqlcmd -b -V16 -U SA -P $MSSQL_SA_PASSWORD -Q "RESTORE DATABASE [$DB_DATABASE] FROM DISK = N'/usr/src/app/dump.bak' WITH FILE = 1, NOUNLOAD, REPLACE, RECOVERY, STATS = 5"

wait "$sqlservr_pid"
