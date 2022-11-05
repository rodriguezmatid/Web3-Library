from web3 import Web3
import json
import dotenv as _dotenv
import os as os

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

routerAddress = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
routerAddress = web3.toChecksumAddress(routerAddress)

routerContract = web3.eth.contract(address = routerAddress, abi = abi_router)
