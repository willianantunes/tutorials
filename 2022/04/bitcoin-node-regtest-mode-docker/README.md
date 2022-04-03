# Bitcoin Node with RegTest mode using Docker

Do you want to know about Bitcoin Node with RegTest mode using Docker? Look at this project 👀!

## Project details

> ⚠ Note that you must add the `-regtest` argument after each `bitcoin-cli` command to correctly access your Regtest environment. If you prefer, you can include a `regtest=1` command in your `~/.bitcoin/bitcoin.conf` file.

At the root folder of the project, just issue the following command:

    UID=$UID GID=$GID docker-compose up bitcoin-core-regtest

Now you are able to create a wallet! Let's create two:
 
    docker-compose exec --user bitcoin bitcoin-core-regtest bitcoin-cli -regtest createwallet "iago"
    docker-compose exec --user bitcoin bitcoin-core-regtest bitcoin-cli -regtest createwallet "jafar"

You can create an address for receiving payments for each wallet, including one more for _jafar_:

    docker-compose exec --user bitcoin bitcoin-core-regtest bitcoin-cli -regtest -rpcwallet=iago getnewaddress
    docker-compose exec --user bitcoin bitcoin-core-regtest bitcoin-cli -regtest -rpcwallet=jafar getnewaddress
    docker-compose exec --user bitcoin bitcoin-core-regtest bitcoin-cli -regtest -rpcwallet=jafar getnewaddress -addresstype p2sh-segwit

Listing all addresses from each wallet:

    docker-compose exec --user bitcoin bitcoin-core-regtest bitcoin-cli -regtest -rpcwallet=iago listreceivedbyaddress 1 true
    docker-compose exec --user bitcoin bitcoin-core-regtest bitcoin-cli -regtest -rpcwallet=jafar listreceivedbyaddress 1 true
    
If you want to explore directly inside the container, just issue the command:

    docker-compose exec --user bitcoin bitcoin-core-regtest sh

## Links

Guides

- https://developer.bitcoin.org/examples/testing.html
- https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line/blob/master/03_3_Setting_Up_Your_Wallet.md
- https://vhernando.github.io/bitcoind-create-wallet-without-private-keys-bitcoin

Utils:

- https://bitcointalk.org/index.php?topic=5211417.0
- https://bitcoin.stackexchange.com/a/37497
- https://github.com/bitcoin/bitcoin/blob/74b011bbfa3b607606cc7c0ce6e2d22cfd07605a/share/examples/bitcoin.conf
- https://bitcointalk.org/index.php?topic=5139623.0
- https://github.com/tekbe/wallet-tools

Tools:

- https://jlopp.github.io/bitcoin-core-config-generator/

## Credits

- https://github.com/ruimarinho/docker-bitcoin-core
- https://github.com/guggero/docker-bitcoin-core-qt
