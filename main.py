from email.headerregistry import Address
from web3 import Web3
import json
import dotenv as _dotenv
import os as os

_dotenv.load_dotenv()

ganache_url = "HTTP://127.0.0.1:7545"
infura_url = os.environ["INFURA_URL"]
web3 = Web3(Web3.HTTPProvider(infura_url))

# Allows you to read information about the blockchain, like the blocks and the transactions, create transactions, and interact with smart contracts
# Log
if web3.isConnected() == True:
    print('Logged in')
else:
    print('Not logged')

# Number of the last block in the blockchain
print("Last block number")
print(web3.eth.blockNumber)
print()

# Eth balance from a wallet
wallet = '0xfcE92BDB5D1bBA58A844Cff9dff8A5e680670Ade'
balance = web3.eth.get_balance(wallet)
print("Wallet balance in ETH")
print(web3.fromWei(balance, 'ether'))
print()

# information of last block
# print(web3.eth.getBlock(web3.eth.blockNumber))

############################################################################################################################################
#################################################################  Token analysis ##########################################################
############################################################################################################################################

# The ABI is a json array that describes the functions on the smart contract
abi = json.loads('[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')
address = "0xd26114cd6EE289AccF82350c8d8487fedB8A0C07"

contract = web3.eth.contract(address=address, abi=abi)
totalSupply = contract.functions.totalSupply().call() # call functions implies reading data from the blockchain

# Protocol name
print("Protocol name: " f"{contract.functions.name().call()}")
# Token
print("Token: " f"{contract.functions.symbol().call()}")
# Total Supply
print("Total Supply: " f"{web3.fromWei(totalSupply, 'ether')}")


# Transactions!!!

account_1 = "0x6F7CdD9890E0Dc4527c3352d5FEA8C3Db78eDFF8"
account_2 = "0xEd37C57F4Bd9d5F9ca2C911d5AA77eC37F1667d6"
private_key = "db3d9a4da2282b2c0a95851e6c7de76fa718b9627cf7f1275cd47157aeb3116c"

# Get the nonce
nonce = web3.eth.getTransactionCount(account_1)

# Build a transaction
tx = {
    'nonce': nonce,
    'to': account_2,
    'value': web3.toWei(1, 'ether'),
    'gas': 20000000000,
    'gasPrice': web3.toWei('50', 'gwei')
}

# Sign transaction
signed_tx = web3.eth.account.signTransaction(tx, private_key)
# Send transaction
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
# Get transaction hash
print(web3.toHex(tx_hash))