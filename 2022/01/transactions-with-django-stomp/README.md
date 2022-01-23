# Transactions with Django STOMP

Do you want to know [how you can use transactions with STOMP through Django STOMP](https://www.willianantunes.com/blog/2022/01/using-transactions-with-stomp-with-the-help-of-django-stomp/)? Look at this project 👀!

## Project details

Before executing the tests in your favorite IDE, don't forget firing up the broker:

    docker-compose up -d rabbitmq

Then you're good to go! Just access `http://localhost:15672/` using `guest:guest` as the credential so you can access [The RabbitMQ management plugin](https://www.rabbitmq.com/management.html).

If you just want to run all the tests with Compose, then you should be good with:

    docker-compose up tests
