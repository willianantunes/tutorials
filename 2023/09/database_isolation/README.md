# Database Isolations

To understand it, please read the article [Understanding Read Phenomena by Practice with MariaDB and PostgreSQL](https://www.willianantunes.com/blog/2023/09/understanding-read-phenomena-by-practice-with-mariadb-and-postgresql/).

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

### Manage packages

    docker-compose run remote-interpreter-mariadb pipenv update
    docker-compose run remote-interpreter-mariadb pipenv install faker

### Generating a new migration

    docker-compose run remote-interpreter-mariadb python manage.py makemigrations

### Retrieving DDL from migration

Don't forget to change `0001` to the migration you want to target:

    docker-compose run remote-interpreter-mariadb python manage.py sqlmigrate core 0001
    docker-compose run remote-interpreter-postgresql python manage.py sqlmigrate core 0001
