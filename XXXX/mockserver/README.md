# MockServer

Just run `docker-compose up` and access the following address:

- http://localhost:1080/mockserver/dashboard

If you need to clear all recorded requests:

```shell
curl -v -X PUT "http://localhost:1080/mockserver/clear?type=log"
```

Check out [more examples](https://www.mock-server.com/mock_server/clearing_and_resetting.html)!

## Doing requests

```shell
curl -i "http://localhost:1080/api/v1/acme"
```

```shell
curl -i "http://localhost:1080/api/v1/qwerty"
```

```shell
curl -i "http://localhost:1080/api/v1/xyz"
```
