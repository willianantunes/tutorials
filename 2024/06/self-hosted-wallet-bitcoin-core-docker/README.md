# Self-hosted wallet setup with Bitcoin Core using Docker

This project is a proof of concept to demonstrate how to set up a self-hosted wallet using two Bitcoin Core nodes, both in pruned mode. One node `bitcoin-core-middleware` acting as a normal node with no max peer connection limit, and the other node called `bitcoin-core-wallet` acting as its name suggests with a max peer connection limit of 1. The middleware node will act as a peer to the wallet node.

The wallet node is the one you must use to interact with the `wallet.dat`. The middleware node is just a peer to the wallet node.

## Before you start

Generate the `rpcauth` string to be appended to the `bitcoin.conf` file.

```shell
python rpcauth.py jaffar
python rpcauth.py jasmine
```

Sample output:

```text
String to be appended to bitcoin.conf:
rpcauth=jafar:4fa794addec8e955123456ab93cf137c$279369610574dc4059ce1fd36b9232702ff8b8429fe6490dc856c0db02119795
Your password:
CYa-7c9-M_0_va3Qg_3vJHaimN-kiM

String to be appended to bitcoin.conf:
rpcauth=jasmine:3b821b7$17b114961abb15e83421856067a3843c15cb29fe259afaeda177b023
Your password:
Llc5yNHoZGrF4ctPPh_12dCg
```

Configure the generated `rpcauth` string in the `bitcoin.conf` file. Store the password in a secure location.

## Important notice about blockchain data

If possible copy the entire blockchain data from someone else to avoid downloading it from scratch. Let's say you have it, then you just copy the folder and paste it with the name `bitcoin-core-middleware` somewhere. Now you can create a volume to mount the folder to the container. Don't forget to copy the provided [`bitcoin.conf`](./middleware/bitcoin.conf) file to the folder. Example:

```yaml
  bitcoin-core-middleware:
    build:
      context: .
    volumes:
      - "/tmp/bitcoin_core_middleware:/home/bitcoin/.bitcoin/"
    environment:
      - UID=$UID
      - GID=$GID
```

Run the service and wait for its full synchronization until it's fully pruned. Now you can copy the folder and paste it with the name `bitcoin-core-wallet`. Again, don't forget to copy the provided [`bitcoin.conf`](./wallet/bitcoin.conf) file to the folder. Example:

```yaml
  bitcoin-core-wallet:
    build:
      context: .
    volumes:
      - "/tmp/bitcoin_core_wallet:/home/bitcoin/.bitcoin/"
    environment:
      - UID=$UID
      - GID=$GID
```

## Running the project

At the root folder of the project, just issue the following command:

    UID=$UID GID=$GID docker compose up bitcoin-core-middleware

Now spin up the wallet container:

    UID=$UID GID=$GID docker compose up bitcoin-core-wallet

It will add the middleware as peer to the wallet bitcoin-core node. 

## Interacting with the wallet

Given you have the `wallet.dat` file inside the `/home/bitcoin/.bitcoin/` folder in `bitcoin-core-wallet` container, you can interact with the wallet using the `bitcoin-cli` command. Execute the following command to get the balance of the wallet:

```shell
UID=$UID GID=$GID docker compose run bitcoin-core-wallet \
bitcoin-cli \
-rpcconnect=bitcoin-core-wallet \
-rpcuser=jasmine \
-stdinrpcpass \
getbalance
```

You'll have to enter the password generated earlier.

## Exploring the container

If you want to explore directly inside the container, just issue the command:

    UID=$UID GID=$GID docker compose run bitcoin-core-middleware bash

## Links

- https://en.bitcoin.it/wiki/Running_Bitcoin#Bitcoin.conf_Configuration_File
