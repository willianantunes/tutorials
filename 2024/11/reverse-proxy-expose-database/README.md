# Reverse proxy your database

To understand it, please read the article [Reverse Proxy Your Database](https://www.willianantunes.com/blog/2024/11/reverse-proxy-your-database/).

## Running the project

Execute the following command:

```shell
docker compose up
```

Use your favorite database client with ssl mode as `require` and connect directly to the database at `localhost:5432`. To use the reverse proxy, connect to `localhost:7000`.
