from web3 import Web3
import json
import dotenv as _dotenv
import os as os
import time

_dotenv.load_dotenv()

ganache_url = "HTTP://127.0.0.1:7545"
infura_url = os.environ["INFURA_URL"]
web3 = Web3(Web3.HTTPProvider(infura_url))

# Log
if web3.isConnected() == True:
    print('Logged in')
else:
    print('Not logged')
print()

# ABI's
with open('./utils/contract_factory.json', 'r') as f:
  abi_contract_factory = json.load(f)

with open('./utils/pools.json', 'r') as f:
  abi_pools = json.load(f)

with open('./utils/router.json', 'r') as f:
    abi_router = json.load(f)

factoryAddress = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
routerAddress = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
wethAddress = '0xDf032Bc4B9dC2782Bb09352007D4C57B75160B15'
account = '0x596FbF10a5129fa7ae38FD6135C0954d415ea7Bc'
routerAddress = web3.toChecksumAddress(routerAddress)

routerContract = web3.eth.contract(address = routerAddress, abi = abi_router)

# Get the nonce // prevents you of sending a tx twice
nonce = web3.eth.getTransactionCount(account)

swap = routerContract.functions.swapExactTokensForTokens(
          1, #uint amountIn
          0, #uint amountOutMin
          [token1Address, token2Address],#address[] calldata path
          account,#address to
          int(time.time()) + (60*1)#uint deadline
          ).buildTransaction({
            'nonce': nonce,
            'from': account,
            'value': web3.toWei(1, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
          })

# Sign transaction
signed_tx = web3.eth.account.signTransaction(swap, private_key)

# Send transaction
send_tx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

# Get transaction hash
print(web3.toHex(send_tx))