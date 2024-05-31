# Ethereum proof of stake development network

This is a copy of [OffchainLabs/eth-pos-devnet](https://github.com/OffchainLabs/eth-pos-devnet) with some changes. Check out its [main article](https://rauljordan.com/how-to-setup-a-proof-of-stake-devnet/). The main difference is that Geth is not used to manage accounts, but Clef is used instead. The latter is the recommended way to manage accounts according to the [official documentation](https://geth.ethereum.org/docs/fundamentals/account-management).

First you must initialize Clef. Execute the following command:

    docker compose run gethtools sh

Execute `clef init` and configure the master seed. If you want to use the current [`masterseed.json`](./account-manager/masterseed.json), its password is `1234567890`. Then you can start the Clef service:

    clef --chainid 32382 --loglevel 6 --http --http.addr=0.0.0.0

The chain ID configured in the file [execution/genesis.json](./execution/genesis.json) must be the same, that is why we used `32382`.

Take the container's IP address with the command `docker inspect CONTAINER_ID | grep IPAddress` and replace the placeholder `CLEF_CONTAINER_IP_ADDRESS` in the file [docker-compose.yaml](./docker-compose.yml). If the IP is `192.168.80.2`, the line will be `--signer=http://192.168.80.2:8550`. 

Now we can spin up the Ethereum proof of stake development network. Execute the following command:

    docker compose up validator beacon-chain geth

You can proceed to interact with it.

## Geth and Clef

### How to create an account

Execute the following command:

    docker compose run gethtools sh

Then issue the following command:

    clef --chainid 32382 newaccount

### Listing accounts

    docker compose run geth --datadir /execution attach

Then you list all accounts executing:

    eth.accounts

On the Clef terminal, you'll see a message like this:

```
A request has been made to list all accounts. 
You can select which accounts the caller can see
  [x] 0x123463a4B065722E99115D6c222f267d9cABb524
    URL: keystore:///root/.ethereum/keystore/UTC--2022-08-19T17-38-31.257380510Z--123463a4b065722e99115d6c222f267d9cabb524
  [x] 0x25815ef1C6Eb80D88A5E31412022B8870B7B1C43
    URL: keystore:///root/.ethereum/keystore/UTC--2024-05-30T21-30-23.388457648Z--25815ef1c6eb80d88a5e31412022b8870b7b1c43
  [x] 0x646a916f656F39e1EFA98d4D8eBA2BBdb7C6779B
    URL: keystore:///root/.ethereum/keystore/UTC--2024-05-30T21-31-02.131044750Z--646a916f656f39e1efa98d4d8eba2bbdb7c6779b
  [x] 0xC0802Cace6c5Ed6a58b8D27E9991aDeD3BD0e546
    URL: keystore:///root/.ethereum/keystore/UTC--2024-05-31T16-00-49.547032179Z--c0802cace6c5ed6a58b8d27e9991aded3bd0e546
-------------------------------------------
Request context:
	192.168.80.4:40264 -> http -> 192.168.80.2:8550

Additional HTTP header data, provided by the external caller:
	User-Agent: "Go-http-client/1.1"
	Origin: ""
Approve? [y/N]:
```

Type `y` and press `Enter`. Now you can list the accounts.

### Checking balance

Know how much ether you have:

    web3.fromWei(eth.getBalance(eth.accounts[0]), "ether")
    web3.fromWei(eth.getBalance(eth.accounts[1]), "ether")
    web3.fromWei(eth.getBalance(eth.accounts[2]), "ether")

For each command you'll have to approve the request on the Clef terminal.

### Sending ether

Send some ether to another account:

```javascript
eth.getTransaction(
    web3.eth.sendTransaction(
        {
            from: eth.accounts[0],
            to: eth.accounts[1],
            value: web3.toWei(0.5, 'ether')
        }
    )
)
```

The password for the account `eth.accounts[0]` is an empty string. Approve the request on the Clef terminal again.

The key `blockNumber` will be `null` until the transaction is mined. Example:

```json
{
  "accessList": [],
  "blockHash": null,
  "blockNumber": null,
  "chainId": "0x7e7e",
  "from": "0x123463a4b065722e99115d6c222f267d9cabb524",
  "gas": 21000,
  "gasPrice": 3000000000,
  "hash": "0xf7a2c5ec2b44f99b159876efb0254ba87f8def7e43a2afcc29232544cbe16691",
  "input": "0x",
  "maxFeePerGas": 3000000000,
  "maxPriorityFeePerGas": 1000000000,
  "nonce": 0,
  "r": "0x25101edad9141ebe5305df494627afc079c0d6298277038084a89916e6dd4925",
  "s": "0x2a4c75f595abd8f6d6f4cdbd2bdcdf5634ac75d011ff4c71fa6e724ea1b87d14",
  "to": "0x25815ef1c6eb80d88a5e31412022b8870b7b1c43",
  "transactionIndex": null,
  "type": "0x2",
  "v": "0x0",
  "value": 500000000000000000,
  "yParity": "0x0"
}
```

As soon as it's mined, the key `blockNumber` will have the block number. If you execute:

    eth.getTransaction("0xf7a2c5ec2b44f99b159876efb0254ba87f8def7e43a2afcc29232544cbe16691")

Now you'll get the following, for example:

```json
{
  "accessList": [],
  "blockHash": "0x6a62924efeecc56af3bebb1244995973de0c4202f2c94b05b6b38b1318d76477",
  "blockNumber": 1,
  "chainId": "0x7e7e",
  "from": "0x123463a4b065722e99115d6c222f267d9cabb524",
  "gas": 21000,
  "gasPrice": 1875000000,
  "hash": "0xf7a2c5ec2b44f99b159876efb0254ba87f8def7e43a2afcc29232544cbe16691",
  "input": "0x",
  "maxFeePerGas": 3000000000,
  "maxPriorityFeePerGas": 1000000000,
  "nonce": 0,
  "r": "0x25101edad9141ebe5305df494627afc079c0d6298277038084a89916e6dd4925",
  "s": "0x2a4c75f595abd8f6d6f4cdbd2bdcdf5634ac75d011ff4c71fa6e724ea1b87d14",
  "to": "0x25815ef1c6eb80d88a5e31412022b8870b7b1c43",
  "transactionIndex": 0,
  "type": "0x2",
  "v": "0x0",
  "value": 500000000000000000,
  "yParity": "0x0"
}
```

You can also check the transaction receipt when it's mined:

    eth.getTransactionReceipt("0xf7a2c5ec2b44f99b159876efb0254ba87f8def7e43a2afcc29232544cbe16691")

Sample output:

```json
{
  "blockHash": "0x6a62924efeecc56af3bebb1244995973de0c4202f2c94b05b6b38b1318d76477",
  "blockNumber": 1,
  "contractAddress": null,
  "cumulativeGasUsed": 21000,
  "effectiveGasPrice": 1875000000,
  "from": "0x123463a4b065722e99115d6c222f267d9cabb524",
  "gasUsed": 21000,
  "logs": [],
  "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
  "status": "0x1",
  "to": "0x25815ef1c6eb80d88a5e31412022b8870b7b1c43",
  "transactionHash": "0xf7a2c5ec2b44f99b159876efb0254ba87f8def7e43a2afcc29232544cbe16691",
  "transactionIndex": 0,
  "type": "0x2"
}
```

### Sending ether from an account that requires a password

If you do the following:

```javascript
web3.eth.sendTransaction(
    {
        from: eth.accounts[1],
        to: eth.accounts[2],
        value: web3.toWei(0.02, 'ether')
    }
)
```

The password for the account `eth.accounts[1]` is in the file [account-manager/keystore/25815-pass.txt](./account-manager/keystore/25815-pass.txt). Approve the request on the Clef terminal again.

## web3py

Your proof of stake development network must be running. If so, execute `poetry install` and then you can run the file [`account_operations.py`](./account_operations.py). Change how it interacts with the network by modifying the file as you wish. Then execute:

    poetry run python account_operations.py

Sample output:

```text
Is connected to the network:  True
Middleware injected because some specific protocols given some ExtraBytes in the response.
Gathering all accounts details
Account 0x123463a4B065722E99115D6c222f267d9cABb524 has been loaded. Current balance: 19999.500020429262021 ETH
Account 0x25815ef1C6Eb80D88A5E31412022B8870B7B1C43 has been loaded. Current balance: 0.489978999999853 ETH
Account 0x646a916f656F39e1EFA98d4D8eBA2BBdb7C6779B has been loaded. Current balance: 0.01 ETH
Get and determine gas parameters
Defining the transaction parameters
Explorer link Mainnet: https://etherscan.io/tx/0x5dcd1eafe355d703401f3e8e2cac5ad1d169f60125605b7b11433e1052b4638e
Transaction receipt: AttributeDict({'blockHash': HexBytes('0x10d3efbda638eabfbb3a230410c703bb0a742201a60be5047842ce243dfd5f61'), 'blockNumber': 818, 'contractAddress': None, 'cumulativeGasUsed': 21000, 'effectiveGasPrice': 1000000007, 'from': '0x123463a4B065722E99115D6c222f267d9cABb524', 'gasUsed': 21000, 'logs': [], 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'), 'status': 1, 'to': '0x646a916f656F39e1EFA98d4D8eBA2BBdb7C6779B', 'transactionHash': HexBytes('0x5dcd1eafe355d703401f3e8e2cac5ad1d169f60125605b7b11433e1052b4638e'), 'transactionIndex': 0, 'type': 2})
Get and determine gas parameters
Defining the transaction parameters
Explorer link Mainnet: https://etherscan.io/tx/0x49116b6f365f56903062b52b8a6390cb0d0ef0abe5d97ab88cfa0ba514eb22c3
Transaction receipt: AttributeDict({'blockHash': HexBytes('0x45ca254db2a48d5fb5a0128c21a2321e64b785031da4a9a61a65b0e8785f2e9e'), 'blockNumber': 819, 'contractAddress': None, 'cumulativeGasUsed': 21000, 'effectiveGasPrice': 1000000007, 'from': '0x123463a4B065722E99115D6c222f267d9cABb524', 'gasUsed': 21000, 'logs': [], 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'), 'status': 1, 'to': '0x646a916f656F39e1EFA98d4D8eBA2BBdb7C6779B', 'transactionHash': HexBytes('0x49116b6f365f56903062b52b8a6390cb0d0ef0abe5d97ab88cfa0ba514eb22c3'), 'transactionIndex': 0, 'type': 2})
Get and determine gas parameters
Defining the transaction parameters
Explorer link Mainnet: https://etherscan.io/tx/0xa258f78d34f3d25c063ee4cc4987c1d138d3937dbcf42edfce94a0e3ae9827e2
Transaction receipt: AttributeDict({'blockHash': HexBytes('0xa055ac00bf9108026b8f259b4079a12ddad20c669ab1e635133637e25f401ed6'), 'blockNumber': 820, 'contractAddress': None, 'cumulativeGasUsed': 21000, 'effectiveGasPrice': 1000000007, 'from': '0x123463a4B065722E99115D6c222f267d9cABb524', 'gasUsed': 21000, 'logs': [], 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'), 'status': 1, 'to': '0x646a916f656F39e1EFA98d4D8eBA2BBdb7C6779B', 'transactionHash': HexBytes('0xa258f78d34f3d25c063ee4cc4987c1d138d3937dbcf42edfce94a0e3ae9827e2'), 'transactionIndex': 0, 'type': 2})
```

## Destroy the network

Stop all containers then execute:

    docker compose down -t 0

Run the script [clean.sh](./clean.sh) to remove all files created by the network. If an error `Permission denied` occurs, execute `sudo chown -R YOUR_OWNER:YOUR_GROUP .` and then run the script again.
