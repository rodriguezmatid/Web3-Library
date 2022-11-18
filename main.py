from web3 import Web3
import json
import dotenv as _dotenv
import os as os

_dotenv.load_dotenv()

# ##########################
# ###### Mainnet ######
# ##########################
infura_url = os.environ["INFURA_URL"]
web3 = Web3(Web3.HTTPProvider(infura_url))

# ##########################
# ###### Testnet ###########
# ##########################
#web3 = Web3(Web3.HTTPProvider(os.environ['GOERLI_URL']))
#privateKey = os.environ['GOERLI_PRIVATE_KEY']

# Allows you to read information about the blockchain, like the blocks and the transactions, create transactions, and interact with smart contracts
# Log
if web3.isConnected() == True:
    print('Logged in')
else:
    print('Not logged')

############################################################################################################################################
#################################################################  Address #################################################################
############################################################################################################################################

address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"

# ############################################################################################################################################
# #################################################################  ABI's ###################################################################
# ############################################################################################################################################

with open('./utils/contract_factory.json', 'r') as f:
  abi_contract_factory = json.load(f)

with open('./utils/pools.json', 'r') as f:
  abi_pools = json.load(f)

with open('./utils/router.json', 'r') as f:
    abi_router = json.load(f)

# # # Number of the last block in the blockchain
# #print("Last block number")
# #print(web3.eth.blockNumber)
# #print()

# Eth balance from a wallet
wallet = '0xfcE92BDB5D1bBA58A844Cff9dff8A5e680670Ade'
balance = web3.eth.get_balance(wallet)

print("Wallet balance in ETH")
print(web3.fromWei(balance, 'ether'))
print()

# # # information of last block
# # print(web3.eth.getBlock(web3.eth.blockNumber))

# ############################################################################################################################################
# #################################################################  Token analysis ##########################################################
# ############################################################################################################################################
contract = web3.eth.contract(address=address, abi=abi_pools)
# totalSupply = contract.functions.totalSupply().call() # call functions implies reading data from the blockchain

# # Protocol name
# print("Protocol name: " f"{contract.functions.name().call()}")
# # Token
# print("Token: " f"{contract.functions.symbol().call()}")
# # Total Supply
# print("Total Supply: " f"{web3.fromWei(totalSupply, 'ether')}")

daibalance = contract.functions.balanceOf(wallet).call()
print(web3.fromWei(daibalance, 'ether'))
print()

# ############################################################################################################################################
# #################################################################  Transaction ##########################################################
# ############################################################################################################################################
# # account = web3.toChecksumAddress('0x596FbF10a5129fa7ae38FD6135C0954d415ea7Bc')
# # account_2 = web3.toChecksumAddress('0x5144C21864E24235E81F7e8c4a8d60663666eA94')

# # # Get the nonce // prevents you of sending a tx twice
# # nonce = web3.eth.getTransactionCount(account)

# # # Build a transaction
# # tx = {
# #     'nonce': nonce,
# #     'to': account_2,
# #     'value': web3.toWei(0.01, 'ether'),
# #     'gas': 200000,
# #      'gasPrice': web3.eth.gas_price
# #     #'gasPrice': web3.toWei('2', 'gwei')
# # }

# # # Sign transaction
# # signed_tx = web3.eth.account.signTransaction(tx, privateKey)
# # # Send transaction
# # tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
# # # Get transaction hash
# # print(web3.toHex(tx_hash))