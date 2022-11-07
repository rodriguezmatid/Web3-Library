from web3 import Web3
import json
import dotenv as _dotenv
import os as os
import time

_dotenv.load_dotenv()

ganache_url = "HTTP://127.0.0.1:7545"
infura_url = os.environ["INFURA_URL"]
web3 = Web3(Web3.HTTPProvider(infura_url))
privateKey = os.environ['PRIVATE_KEY']

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

# Address
factoryAddress = web3.toChecksumAddress('0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f')
routerAddress = web3.toChecksumAddress('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
wethAddress = web3.toChecksumAddress('0xDf032Bc4B9dC2782Bb09352007D4C57B75160B15')
account = web3.toChecksumAddress('0x596FbF10a5129fa7ae38FD6135C0954d415ea7Bc')

# Contracts
contractFactory = web3.eth.contract(address = factoryAddress, abi = abi_contract_factory)
routerContract = web3.eth.contract(address = routerAddress, abi = abi_router)

# Quantity of pools
poolslength = contractFactory.functions.allPairsLength().call()
counter = 0

for pool in range(0, 1):
  counter += 1

  walletPool = web3.toChecksumAddress(contractFactory.functions.allPairs(pool).call())

  poolContract = web3.eth.contract(address = walletPool, abi = abi_pools)
  token1Address = web3.toChecksumAddress(poolContract.functions.token0().call())
  token2Address = web3.toChecksumAddress(poolContract.functions.token1().call())

  contract1 = web3.eth.contract(address = token1Address, abi = abi_pools)
  contract2 = web3.eth.contract(address = token2Address, abi = abi_pools)

  tokenBalance = poolContract.functions.getReserves().call()

  tokenRatio = tokenBalance[1]/tokenBalance[0]

  token1Symbol = contract1.functions.symbol().call()
  token2Symbol = contract2.functions.symbol().call()

  print("Pool number #" + f"{counter}")
  print(walletPool)
  print("Token Ratio: " + f"{tokenRatio}")
  print()

  #### Token 1 ####
  print(token1Symbol)
  print("Address token 1: " + f"{token1Address}")
  print("# Tokens: " + f"{web3.fromWei(tokenBalance[0], 'ether')}")
  print()

  #### Token 2 ####
  print(token2Symbol)
  print("Address token 2: " + f"{token2Address}")
  print("# Tokens: " + f"{web3.fromWei(tokenBalance[1], 'ether')}")
  print()

# # Get the nonce // prevents you of sending a tx twice
nonce = web3.eth.getTransactionCount(account)

swap = routerContract.functions.swapExactTokensForTokens(
          1, #uint amountIn
          0, #uint amountOutMin
          [token1Address, token2Address], #address[] calldata path
          account, #address to
          int(time.time()) + (60*1) #uint deadline
          ).buildTransaction({
            'nonce': nonce,
            'from': account,
            'value': web3.toWei(1, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
          })

addLiquidity = routerContract.functions.addLiquidity(
          token1Address, # address tokenA,
          token2Address, # address tokenB,
          # uint amountADesired,
          # uint amountBDesired,
          # uint amountAMin,
          # uint amountBMin,
          # address to,
          int(time.time()) + (60*1) # uint deadline
          ).buildTransaction({
            'nonce': nonce,
            'from': account,
            'value': web3.toWei(1, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
          })

removeLiquidity = routerContract.functions.removeLiquidity(
          token1Address, # address tokenA,
          token2Address, # address tokenB,
          # uint liquidity,
          # uint amountAMin,
          # uint amountBMin,
          # address to,
          int(time.time()) + (60*1) # uint deadline
          ).buildTransaction({
            'nonce': nonce,
            'from': account,
            'value': web3.toWei(1, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
          })


# # Sign transaction
# signed_tx = web3.eth.account.signTransaction(swap, privateKey)

# # Send transaction
# send_tx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

# # Get transaction hash
# print(web3.toHex(send_tx))