# Caching JWKS using Redis with Django

Do you want to know about Caching JWKS using Redis with Django? Look at this project 👀!

## Project details

If you just want to run all the tests with Compose, then you should be good with:

    docker-compose up tests

## Exploring Redis

First, fire up the Redis service:

    docker-compose up -d redis

To enter in `redis` service:

    docker-compose run redis sh. 

If it's ready to accept connections, you can connect to it using `redis-cli`:

    redis-cli -h redis -p 6379 -a "this-is-your-admin-password"

Being connected, you can retrieve all existing keys:

    redis:6379> KEYS *
    1) ":1:MY_APP_NAME_JWKS"

Let's retrieve the value for `:1:MY_APP_NAME_JWKS` key:

    redis:6379> GET ":1:MY_APP_NAME_JWKS"
    "\x80\x05\x95\x0f\x00\x00\x00\x00\x00\x00\x00\x8c\x0bsalt-licker\x94."
