# Django Gunicorn Gevent

To understand it, please read the article [Understand Async Workers by Practice with Django, Gunicorn, and Gevent](https://www.willianantunes.com/blog/2023/07/understand-async-workers-by-practice-with-django-gunicorn-and-gevent/).

## Recurring procedures

### Installing new packages and their updates

    docker-compose run remote-interpreter poetry update

### Generating a new migration

    docker-compose run remote-interpreter python manage.py makemigrations

## Notes

    docker run --rm -it --entrypoint /bin/sh williamyeh/hey
    ./hey --help
    http GET :8001/api/v1/movies
    http GET :8000/only-http-call/
    http GET :8000/both-http-and-database-calls/
