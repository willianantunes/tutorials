# C# Web API: How to call your endpoint through integration tests

Read the explanations on [this blog post](https://www.willianantunes.com/blog/2021/05/c-web-api-how-to-call-your-endpoint-through-integration-tests/).

## Project details

If you'd like to run the project, just issue the following command:

    docker-compose up app

Then, with `HTTPie`, you can call the endpoint through `http GET :8000/api/v1/movies`. To illustrate:

```shell
▶ http GET :8000/api/v1/movies
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Date: Wed, 26 May 2021 18:31:38 GMT
Server: Kestrel
Transfer-Encoding: chunked

{
    "duration": "20m",
    "genres": [
        "Action"
    ],
    "release": "01/21/2000",
    "title": "The World of Dragon Ball Z"
}
```

To run the tests:

    docker-compose up tests
