# Self-hosted wallet setup with Bitcoin Core using Docker

To understand it, please read the article [Self-hosted wallet setup with Bitcoin Core using Docker](https://www.willianantunes.com/blog/2024/06/self-hosted-wallet-setup-with-bitcoin-core-using-docker/).

## Exploring the container

If you want to explore directly inside the container, just issue the command:

    UID=$UID GID=$GID docker compose exec bitcoin-core-middleware bash
    UID=$UID GID=$GID docker compose exec bitcoin-core-wallet bash
