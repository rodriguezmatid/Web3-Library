from web3 import Web3
import json
import dotenv as _dotenv
import os as os
import time

_dotenv.load_dotenv()

web3 = Web3(Web3.HTTPProvider(os.environ['GOERLI_URL']))
privateKey = os.environ['GOERLI_PRIVATE_KEY']

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

# Address v2
factoryAddress = web3.toChecksumAddress('0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f')
routerAddress = web3.toChecksumAddress('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
account = web3.toChecksumAddress('0x596FbF10a5129fa7ae38FD6135C0954d415ea7Bc')
poolAddress = web3.toChecksumAddress('0x186b57aFFE222D6176347D338Ed66Ea2e20D630d')

daiAddress = web3.toChecksumAddress('0xdc31ee1784292379fbb2964b3b9c4124d8f89c60')
usdcAddress = web3.toChecksumAddress('0x07865c6e87b9f70255377e024ace6630c1eaa37f')
wethAddress = web3.toChecksumAddress('0xb4fbf271143f4fbf7b91a5ded31805e42b2208d6')

contractFactory = web3.eth.contract(address = factoryAddress, abi = abi_contract_factory)
routerContract = web3.eth.contract(address = routerAddress, abi = abi_router)
poolContract = web3.eth.contract(address = poolAddress, abi = abi_pools)

# direcpool = web3.toChecksumAddress(contractFactory.functions.getPair(wethAddress,daiAddress).call())
# print(direcpool)

token1Address = web3.toChecksumAddress(poolContract.functions.token0().call())
token2Address = web3.toChecksumAddress(poolContract.functions.token1().call())

contract1 = web3.eth.contract(address = token1Address, abi = abi_pools)
contract2 = web3.eth.contract(address = token2Address, abi = abi_pools)

tokenBalance = poolContract.functions.getReserves().call()

token1Symbol = contract1.functions.symbol().call()
token2Symbol = contract2.functions.symbol().call()

print(poolAddress)
print()

## Token 1 ####
print(token1Symbol)
print("Address token 1: " + f"{token1Address}")
print("# Tokens: " + f"{web3.fromWei(tokenBalance[0], 'ether')}")
print()

## Token 2 ####
print(token2Symbol)
print("Address token 2: " + f"{token2Address}")
print("# Tokens: " + f"{web3.fromWei(tokenBalance[1], 'ether')}")
print()

# # Get the nonce // prevents you of sending a tx twice
nonce = web3.eth.getTransactionCount(account)

allowance1 = contract1.functions.allowance(account, routerAddress).call()
allowance2 = contract2.functions.allowance(account, routerAddress).call()
print("Allowance 1: " + f"{allowance1}")
print("Allowance 2: " + f"{allowance2}")

if allowance1 == 0:
  approval = contract1.functions.approve(routerAddress,web3.toWei(10000000, 'ether')).buildTransaction({
     "nonce": nonce,
     "from": account,
     "gas": 200000,
     'gasPrice': web3.eth.gas_price
  })
  signed_approval = web3.eth.account.signTransaction(approval, privateKey)
  print(web3.toHex(web3.eth.sendRawTransaction(signed_approval.rawTransaction)))
  nonce += 1

if allowance2 == 0:
  approval = contract2.functions.approve(routerAddress,web3.toWei(10000000, 'ether')).buildTransaction({
     "nonce": nonce,
     "from": account,
     "gas": 200000,
     'gasPrice': web3.eth.gas_price
  })
  signed_approval = web3.eth.account.signTransaction(approval, privateKey)
  print(web3.toHex(web3.eth.sendRawTransaction(signed_approval.rawTransaction)))
  nonce += 1

swap = routerContract.functions.swapExactTokensForTokens(
            web3.toWei(0.01, 'ether'), #uint amountIn,
            0, # uint amountOutMin,
            [token1Address, token2Address], #address[] calldata path
            account, #address to
            int(time.time()) + (60) #uint deadline
            ).buildTransaction({
              "nonce": nonce,
              'from': account,
              'gas': 200000,
              'gasPrice': web3.eth.gas_price
              #'gasPrice': web3.toWei('2', 'gwei')
            })

# Sign transaction
signed_tx = web3.eth.account.signTransaction(swap, privateKey)
# Send transaction
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
# Get transaction hash
print(web3.toHex(tx_hash))