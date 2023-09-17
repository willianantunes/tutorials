# Database Isolations

I'll just cover the basics. For a business developer I think that's crucial, though you can go a lot deeper. It's worth mentioning that the isolation level in MariaDB is `REPEATABLE READ` by default. Know more in the [knowledge base](https://mariadb.com/kb/en/mariadb-transactions-and-isolation-levels-for-sql-server-users/#isolation-levels-and-locks).

## Understanding read phenomena by practice in MariaDB

You start with the following command:

```shell
docker-compose up db-mariadb
```

When it's up and running, you can issue the following in another terminal:

```shell
docker-compose run terminal-mariadb
```

Then connect to the database instance using [MariaDB CLI](https://mariadb.com/kb/en/mysql-command-line-client/):

```shell
mariadb -u root -p'root' \
-h db-mariadb -P 3306 \
-D development
```

For each `TX XYZ` you can open a terminal and proceeds with the mentioned steps above.

### Dirty read

It's when you read a row that has not been committed yet by another transaction. What if the other transaction decides to rollback while your transaction continues with its processing using the dirty read?

TX 1:

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN;
SELECT * FROM `core_account` WHERE `core_account`.`username` = 'ysullivan';
```

Output:

```text
+----------------------------------+----------------------------+----------------------------+-----------+-----------+
| id                               | created_at                 | updated_at                 | username  | balance   |
+----------------------------------+----------------------------+----------------------------+-----------+-----------+
| bad19496526b4cf3831ad4a8244eecf1 | 2023-09-22 00:20:55.377114 | 2023-09-22 00:20:55.377144 | ysullivan | 1000.0000 |
+----------------------------------+----------------------------+----------------------------+-----------+-----------+
```

TX 2:

```sql
BEGIN;
UPDATE core_account SET balance = 1001.0000 WHERE username = 'ysullivan';
```

TX 1:

```
SELECT * FROM `core_account` WHERE `core_account`.`username` = 'ysullivan';
```

You'll get `1001`, though the TX 2 hasn't been committed yet:

```text
+----------------------------------+----------------------------+----------------------------+-----------+-----------+
| id                               | created_at                 | updated_at                 | username  | balance   |
+----------------------------------+----------------------------+----------------------------+-----------+-----------+
| bad19496526b4cf3831ad4a8244eecf1 | 2023-09-22 00:20:55.377114 | 2023-09-22 00:20:55.377144 | ysullivan | 1001.0000 |
+----------------------------------+----------------------------+----------------------------+-----------+-----------+
```

You can run rollback in both transactions by executing `ROLLBACK;`.

### Non-repeatable read

TX 1:

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN;
SELECT SUM(balance) FROM core_account;
```

Output:

```text
+--------------+
| SUM(balance) |
+--------------+
|   55000.0000 |
+--------------+
```

TX 2:

```sql
BEGIN;
UPDATE core_account SET balance = 1001.0000 WHERE username = 'ysullivan';
COMMIT;
```

TX 1:

```sql
SELECT SUM(balance) FROM core_account;
```

You don't get `55000`, but `55001` actually. This is not really a dirty read, this is actual a committed read. We read the value as a certain value, and when we repeat the query, it gives you another value, thus the phenomena name being `non-repeatable read`.

Output:

```text
+--------------+
| SUM(balance) |
+--------------+
|   55001.0000 |
+--------------+
```

### Phantom read

TX 1:

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN;
SELECT COUNT(*), SUM(balance) FROM core_account;
```

Output:

```text
+----------+--------------+
| COUNT(*) | SUM(balance) |
+----------+--------------+
|       10 |   55001.0000 |
+----------+--------------+
```

TX 2:

```sql
BEGIN;
INSERT INTO `core_account` (id, created_at, updated_at, username, balance) VALUES ('735d45b06a174b34bf14b04b0cf6bd27',CURRENT_TIMESTAMP(6),CURRENT_TIMESTAMP(6),'willianantunes',50.0000);
COMMIT;
```

TX 1:

```sql
SELECT COUNT(*), SUM(balance) FROM core_account;
```

We get 11 rows and `55051` when it should be 10 rows and `55001`. One row has been added by another committed transaction, though when `TX 1` started it hadn't this extra row, that's why it's phantom. 

```text
+----------+--------------+
| COUNT(*) | SUM(balance) |
+----------+--------------+
|       11 |   55051.0000 |
+----------+--------------+
```

### Lost updates

You have to do the commands quickly to reproduce the `lost update` phenomena. If you delay to do so, you'll notice that the `TX 2` SQL will block during the update statement until eventually it receives the error `ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction`.

We are not specifying the isolation level, so it will be [REPEATABLE READ](https://mariadb.com/kb/en/set-transaction/#repeatable-read) by default. Check it by executing the command `SELECT @@global.transaction_ISOLATION;`. By the way, repeatable read should not accept lost updates, but [this seems not to be true in MySQL/MariaDB](https://stackoverflow.com/a/10428319/3899136).

TX 1:

```sql
BEGIN;
-- At this point the balance is 1001.0000. In case it's not:
-- UPDATE core_account SET balance = 1001.0000 WHERE username = 'ysullivan';
UPDATE core_account SET balance = balance - 1000.0000 WHERE username = 'ysullivan';
SELECT balance FROM core_account WHERE username = 'ysullivan' FOR UPDATE;
```

Output:

```text
+---------+
| balance |
+---------+
|  1.0000 |
+---------+
```

TX 2:

```sql
BEGIN;
SELECT balance FROM core_account WHERE username = 'ysullivan';
-- The statement below will block, so proceed with the next step as quickly as possible! 
UPDATE core_account SET balance = balance - 501.0000 WHERE username = 'ysullivan';
```

As the output is `1001`, the update statement should result in a balance of `500.0000` in the end. Will it be? Let's see the output before the update statement:

```text
+-----------+
| balance   |
+-----------+
| 1001.0000 |
+-----------+
```

TX 1:

```sql
COMMIT;
SELECT balance FROM core_account WHERE username = 'ysullivan';
```

Output:

```text
+---------+
| balance |
+---------+
|  1.0000 |
+---------+
```

TX 2:

```sql
COMMIT;
SELECT balance FROM core_account WHERE username = 'ysullivan';
```

TX 2's update is lost and in the end we have a negative balance 😱:

```
+-----------+
| balance   |
+-----------+
| -500.0000 |
+-----------+
```

## Understanding read phenomena in PostgreSQL

You start with the following command:

```shell
docker-compose up db-postgresql
```

When it's up and running, you can issue the following in another terminal:

```shell
docker-compose run terminal-postgresql
```

Then connect to the database instance using [PostgreSQL CLI](https://www.postgresql.org/docs/16/index.html):

```shell
psql postgresql://postgres:postgres@db-postgresql:5432/postgres
```

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

### Manage packages

    docker-compose run remote-interpreter-mariadb pipenv update
    docker-compose run remote-interpreter-mariadb pipenv install faker

### Generating a new migration

    docker-compose run remote-interpreter-mariadb python manage.py makemigrations

### Retrieving DDL from migration

Don't forget to change `0001` to the migration you want to target:

    docker-compose run remote-interpreter-mariadb python manage.py sqlmigrate core 0001
    docker-compose run remote-interpreter-postgresql python manage.py sqlmigrate core 0001
