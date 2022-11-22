from web3 import Web3
import json
import dotenv as _dotenv
import os as os
from requests import Session

_dotenv.load_dotenv()

# ##########################
# ###### Mainnet ###########
# ##########################
infura_url = os.environ["INFURA_URL"]
web3 = Web3(Web3.HTTPProvider(infura_url))

if web3.isConnected() == True:
    print('Logged in')
else:
    print('Not logged')

with open('./utils/protocolDataProvider.json', 'r') as f:
    abi_protocolDataProvider = json.load(f)

with open('./utils/lendingPool.json', 'r') as f:
    abi_lendingPool = json.load(f)

with open('./utils/lendingPoolAddressesProviderRegistry.json', 'r') as f:
    abi_lendingPoolAddressesProviderRegistry = json.load(f)

with open('./utils/priceOracle.json', 'r') as f:
    abi_priceOracle = json.load(f)


# ##########################
# ##### CoinmarketCap ######
# ##########################
url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
api_key = os.environ["API_KEY_COINMARKETCAP"]
headers = {
'Accepts': 'application/json',
'X-CMC_PRO_API_KEY': api_key
}
session = Session()
session.headers.update(headers)
parameters = {
'symbol':'ETH',
'convert':'USD'
} # dictionary

response = session.get(url, params=parameters)
ethPrice = json.loads(response.text)['data']['ETH'][0]['quote']['USD']['price']

LendingPoolAddressesProvider = web3.toChecksumAddress('0xb53c1a33016b2dc2ff3653530bff1848a515c8c5')
addressLendingPoolAddressesProviderRegistry = web3.toChecksumAddress('0x52D306e36E3B6B02c153d0266ff0f85d18BCD413')
addressLendingPool = web3.toChecksumAddress('0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9')
LendingPoolCollateralManager = web3.toChecksumAddress('0xbd4765210d4167ce2a5b87280d9e8ee316d5ec7c')
LendingPoolConfigurator = web3.toChecksumAddress('0x311bb771e4f8952e6da169b425e7e92d6ac45756')
LendingRateOracle = web3.toChecksumAddress('0x8a32f49ffba88aba6eff96f45d8bd1d4b3f35c7d')
addressPriceOracle = web3.toChecksumAddress('0xa50ba011c48153de246e5192c8f9258a2ba79ca9')
PoolAdmin = web3.toChecksumAddress('0xee56e2b3d491590b5b31738cc34d5232f378a8d5')
EmergencyAdmin = web3.toChecksumAddress('0xca76ebd8617a03126b6fb84f9b1c1a0fb71c2633')
addressProtocolDataProvider = web3.toChecksumAddress('0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d')
WETHGateway = web3.toChecksumAddress('0xEFFC18fC3b7eb8E676dac549E0c693ad50D1Ce31')
AaveCollector = web3.toChecksumAddress('0x464c71f6c2f760dda6093dcb91c24c39e5d6e18c')
IncentivesController = web3.toChecksumAddress('0xd784927Ff2f95ba542BfC824c8a8a98F3495f6b5')
UiPoolDataProvider = web3.toChecksumAddress('0x30375522F67a6308630d49A694ca1491fA2D3BC6')
UiIncentiveDataProvider = web3.toChecksumAddress('0xD01ab9a6577E1D84F142e44D49380e23A340387d')

wethAddress = web3.toChecksumAddress('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
usdcAddress = web3.toChecksumAddress('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')
daiAddress = web3.toChecksumAddress('0x6B175474E89094C44Da98b954EedeAC495271d0F')
uniAddress = web3.toChecksumAddress('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984')

contractProtocolDataProvider = web3.eth.contract(address = addressProtocolDataProvider, abi = abi_protocolDataProvider)
contractLendingPool = web3.eth.contract(address = addressLendingPool, abi = abi_lendingPool)
contractLendingPoolAddressesProviderRegistry = web3.eth.contract(address = addressLendingPoolAddressesProviderRegistry, abi = abi_lendingPoolAddressesProviderRegistry)
contractPriceOracle = web3.eth.contract(address = addressPriceOracle, abi = abi_priceOracle)

allTokens = contractProtocolDataProvider.functions.getAllReservesTokens().call()
############################################################################################################################################
#################################################################  Total Protocol Pools ####################################################
############################################################################################################################################
i = 0
totalAvaiableLiquidity = 0
totalDebt = 0
for x in allTokens:
    tokenAddress = allTokens[i][1]
    tokenQuantity = contractProtocolDataProvider.functions.getReserveData(tokenAddress).call()
    protocolDataProvider = contractProtocolDataProvider.functions.getReserveConfigurationData(tokenAddress).call()
    decimals = protocolDataProvider[0] # the decimals used by the reserve
    maxLtv = protocolDataProvider[1]/100 # represents the maximum borrowing power of a specific collateral. If a collateral has an LTV of 75%, the user can borrow up to 0.75 worth of ETH in the principal currency for every 1 ETH worth of collateral.
    liquidationThreshold = protocolDataProvider[2]/100 #  threshold at which a borrow position will be considered undercollateralized and subject to liquidation for each collateral
    liquidationPenalty = protocolDataProvider[3]/100 - 100 # bonus awarded to liquidators
    reserveFactor = protocolDataProvider[4]/100 # Reserve factor is a percentage of interest which goes to a collector contract that is controlled by Aave governance to promote ecosystem growth.
    tokenPrice = float(web3.fromWei(contractPriceOracle.functions.getAssetPrice(allTokens[i][1]).call(), 'ether')) * ethPrice
    avaiableLiquidity = round(web3.fromWei(tokenQuantity[0] * tokenPrice, 'ether'), 2)
    stableDebt = round(web3.fromWei(tokenQuantity[1] * tokenPrice, 'ether'), 2)
    variableDebt = round(web3.fromWei(tokenQuantity[2] * tokenPrice, 'ether'), 2)
    tokenDebt = stableDebt + variableDebt
    tokenReserve = tokenDebt + avaiableLiquidity

    totalAvaiableLiquidity = avaiableLiquidity + totalAvaiableLiquidity
    totalDebt = tokenDebt + totalDebt

    print("Asset #", i)
    print(allTokens[i][0])
    print("Token price: ", tokenPrice)
    print("Decimals: ", decimals)
    print("Max LTV: ", maxLtv,"%")
    print("Liquidation threshold: ", liquidationThreshold,"%")
    print("Liquidation penalty: ", liquidationPenalty,"%")
    print("Reserve factor: ", reserveFactor, "%")
    print("Avaiable liquidity: ", avaiableLiquidity)
    print(tokenDebt)
    print(tokenReserve)
    print()

    i = i + 1

############################################################################################################################################
#########################################################################  Pool ############################################################
############################################################################################################################################
# token = uniAddress

# protocolDataProvider = contractProtocolDataProvider.functions.getReserveConfigurationData(token).call()
# decimals = protocolDataProvider[0] # the decimals used by the reserve
# maxLtv = protocolDataProvider[1]/100 # represents the maximum borrowing power of a specific collateral. If a collateral has an LTV of 75%, the user can borrow up to 0.75 worth of ETH in the principal currency for every 1 ETH worth of collateral.
# liquidationThreshold = protocolDataProvider[2]/100 #  threshold at which a borrow position will be considered undercollateralized and subject to liquidation for each collateral
# liquidationPenalty = protocolDataProvider[3]/100 - 100 # bonus awarded to liquidators
# reserveFactor = protocolDataProvider[4]/100 # Reserve factor is a percentage of interest which goes to a collector contract that is controlled by Aave governance to promote ecosystem growth.
# priceInEth = float(web3.fromWei(contractPriceOracle.functions.getAssetPrice(token).call(), 'ether')) * ethPrice
# tokenQuantity = contractProtocolDataProvider.functions.getReserveData(token).call()
# avaiableLiquidity = round(web3.fromWei(tokenQuantity[0]*priceInEth, 'ether'), 2)

# print("Max LTV: ", maxLtv,"%")
# print("Liquidation threshold: ", liquidationThreshold,"%")
# print("Liquidation penalty: ", liquidationPenalty,"%")
# print("Reserve factor: ", reserveFactor, "%")
# print(priceInEth)
# print(web3.fromWei(tokenQuantity[0]*priceInEth, 'ether'))