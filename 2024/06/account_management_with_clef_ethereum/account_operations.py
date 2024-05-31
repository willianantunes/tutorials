import json

from pathlib import Path

from web3 import Web3
from web3.middleware import geth_poa_middleware

chain_id = 32382
rpc_url = "http://localhost:8545"
wallets = "./account-manager/keystore"

account_0 = Path(f"{wallets}/UTC--2022-08-19T17-38-31.257380510Z--123463a4b065722e99115d6c222f267d9cabb524")
account_0_passphrase = Path(f"{wallets}/12346-pass.txt")
account_1 = Path(f"{wallets}/UTC--2024-05-30T21-30-23.388457648Z--25815ef1c6eb80d88a5e31412022b8870b7b1c43")
account_1_passphrase = Path(f"{wallets}/25815-pass.txt")
account_2 = Path(f"{wallets}/UTC--2024-05-30T21-31-02.131044750Z--646a916f656f39e1efa98d4d8eba2bbdb7c6779b")
account_2_passphrase = Path(f"{wallets}/646a9-pass.txt")

web3_client = Web3(Web3.HTTPProvider(rpc_url))
print("Is connected to the network: ", web3_client.is_connected())
web3_client.middleware_onion.inject(geth_poa_middleware, layer=0)
print("Middleware injected because some specific protocols given some ExtraBytes in the response.")


def account_details(account_key_file, account_pass_file):
    with open(account_key_file) as key_file:
        with open(account_pass_file) as passphrase_file:
            account = json.loads(key_file.read())
            account_password = passphrase_file.read().strip()  # Remove the newline character
            account_private_key = web3_client.eth.account.decrypt(account, account_password)
    account_checksum_address = Web3.to_checksum_address(account["address"])
    account_balance = Web3.from_wei(web3_client.eth.get_balance(account_checksum_address), "ether")
    print("Account {} has been loaded. Current balance: {} ETH".format(account_checksum_address, account_balance))
    return {
        "checksum_address": account_checksum_address,
        "private_key": account_private_key,
        "details": account,
    }


print("Gathering all accounts details")
account_0_details = account_details(account_0, account_0_passphrase)
account_1_details = account_details(account_1, account_1_passphrase)
account_2_details = account_details(account_2, account_2_passphrase)


def send_transaction(account_from, account_to, value):
    print("Get and determine gas parameters")  # https://etherscan.io/gastracker
    latest_block = web3_client.eth.get_block("latest")
    base_fee_per_gas_in_wei = latest_block.baseFeePerGas
    max_priority_fee_per_gas = web3_client.to_wei(1, "gwei")  # Priority fee to include the transaction in the block
    max_fee_per_gas = (5 * base_fee_per_gas_in_wei) + max_priority_fee_per_gas  # Maximum amount you’re willing to pay

    print("Defining the transaction parameters")
    transaction = {
        "from": account_from["checksum_address"],
        "to": account_to["checksum_address"],
        "value": Web3.to_wei(value, "ether"),
        "nonce": web3_client.eth.get_transaction_count(account_from["checksum_address"]),
        "gas": 21000,  # Gas limit for the transaction
        "maxFeePerGas": max_fee_per_gas,  # Maximum amount you’re willing to pay
        "maxPriorityFeePerGas": max_priority_fee_per_gas,  # Priority fee to include the transaction in the block
        "chainId": chain_id,
    }
    try:
        transaction = web3_client.eth.account.sign_transaction(transaction, account_from["private_key"])
        transaction_details = web3_client.eth.send_raw_transaction(transaction.rawTransaction)
        print(f"Explorer link Mainnet: https://etherscan.io/tx/{transaction_details.hex()}")
        transaction_receipt = web3_client.eth.wait_for_transaction_receipt(transaction_details)
        print("Transaction receipt:", transaction_receipt)
    except Exception as e:
        if e.args[0]["code"] == -32000:
            print("Address {} has insufficient funds.".format(transaction["from"]))
        message = e.args[0].get("message")
        if message:
            print("Actual error message from the node: {}".format(message))


if __name__ == "__main__":
    send_transaction(account_0_details, account_2_details, 0.5)
    send_transaction(account_0_details, account_2_details, 0.1)
    send_transaction(account_0_details, account_2_details, 0.3)
