# Ethereum Node with Light Mode using Docker

Do you want to know how to create an **Ethereum Node with Light Mode using Docker**? Look at this project 👀!

## Project details

At the root folder of the project, just issue the following command:

    mkdir -p eth && USER=$(id -u) GROUP=$(id -g) docker-compose up

Then you can create an account, for example:

    USER=$(id -u) GROUP=$(id -g) docker-compose run ethereum-geth --datadir /home/aladdin/.ethereum account new

Don't know what to do? Explore it using the help command:

    docker run --rm -it ethereum/client-go:stable --help
