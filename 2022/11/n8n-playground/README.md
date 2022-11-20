# Don't code but automate with N8N

To understand it, please read the article [Don't code but automate with N8N](https://www.willianantunes.com/blog/2022/11/dont-code-but-automate-with-n8n/).

## Project details

Just execute the command:

    docker-compose up

Use the credential `admin:admin` for the following:

- N8N: `http://localhost:5678`. 
- Django ADMIN: `http://localhost:8080/admin`.

## Django

### Retrieving DDL from migration

Don't forget to change `0001` to the migration you want to target:

    docker-compose run app python manage.py sqlmigrate core 0001
