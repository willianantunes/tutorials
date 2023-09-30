# Database Isolations

To understand it, please read the article [Understanding Read Phenomena by Practice with MariaDB and PostgreSQL](https://www.willianantunes.com/blog/2023/09/understanding-read-phenomena-by-practice-with-mariadb-and-postgresql/).

## Recurring procedures

### Dumping database in MariaDB

Supposing `928d81affd34` is your container ID:

```shell
# Inside the container
docker exec -it 928d81affd34 bash
cd /home
exec mariadb-dump --all-databases -uroot -p"$MARIADB_ROOT_PASSWORD" > dump.sql
# In your host machine
docker cp 928d81affd34:/home/dump.sql ./
```

### Dumping database in PostgreSQL

Supposing `7f283827c706` is your container ID:

```shell
# Inside the container
docker exec -it 7f283827c706 bash
cd /home
pg_dump --clean -U postgres -w -h localhost postgres > dump.sql
# In your host machine
docker cp 7f283827c706:/home/dump.sql ./
```

### Dumping database in SQLServer

Supposing `b361ea8ec024` is your container ID:

```shell
# Inside the container
docker exec -it e2242fabc5d0 bash
cd /tmp
# https://learn.microsoft.com/en-us/sql/linux/tutorial-restore-backup-in-sql-server-container?view=sql-server-ver16#copy-a-backup-file-into-the-container
/opt/mssql-tools/bin/sqlcmd -b -V16 -U SA -P $MSSQL_SA_PASSWORD -Q "BACKUP DATABASE [$DB_DATABASE] TO DISK = N'/tmp/dump.bak' with NOFORMAT, NOINIT, NAME = '$DB_DATABASE-full', SKIP, NOREWIND, NOUNLOAD, STATS = 10"
# In your host machine
docker cp e2242fabc5d0:/tmp/dump.bak ./
```

### Manage packages

    docker-compose run remote-interpreter-mariadb pipenv update
    docker-compose run remote-interpreter-mariadb pipenv install faker
    docker-compose run remote-interpreter-mariadb pipenv install mssql-django

### Generating a new migration

    docker-compose run remote-interpreter-mariadb python manage.py makemigrations

### Retrieving DDL from migration

Don't forget to change `0001` to the migration you want to target:

    docker-compose run remote-interpreter-mariadb python manage.py sqlmigrate core 0001
    docker-compose run remote-interpreter-postgresql python manage.py sqlmigrate core 0001
    docker-compose run remote-interpreter-sqlserver python manage.py sqlmigrate core 0001
