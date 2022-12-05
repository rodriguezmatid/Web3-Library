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

contractProtocolDataProvider = web3.eth.contract(address = addressProtocolDataProvider, abi = abi_protocolDataProvider)
contractLendingPool = web3.eth.contract(address = addressLendingPool, abi = abi_lendingPool)
contractLendingPoolAddressesProviderRegistry = web3.eth.contract(address = addressLendingPoolAddressesProviderRegistry, abi = abi_lendingPoolAddressesProviderRegistry)
contractPriceOracle = web3.eth.contract(address = addressPriceOracle, abi = abi_priceOracle)

allTokens = contractProtocolDataProvider.functions.getAllReservesTokens().call()
############################################################################################################################################
#################################################################  Total Protocol Pools ####################################################
############################################################################################################################################
i = 0
totalAvaiableLiquidityUSD = 0
totalBorrowedUSD = 0
totalReserveUSD = 0
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
    # Liquidity
    avaiableLiquidity = tokenQuantity[0]/(10**decimals)
    avaiableLiquidityUSD = avaiableLiquidity * tokenPrice
    # Borrowed
    tokenBorrowed = (tokenQuantity[1] + tokenQuantity[2])/(10**decimals)
    tokenBorrowedUSD = tokenBorrowed * tokenPrice
    # Reserve
    tokenReserve = tokenBorrowed + avaiableLiquidity
    tokenReserveUSD = tokenBorrowedUSD + avaiableLiquidityUSD

    utilizationRate = tokenBorrowedUSD/tokenReserveUSD

    totalAvaiableLiquidityUSD = avaiableLiquidityUSD + totalAvaiableLiquidityUSD
    totalBorrowedUSD = tokenBorrowedUSD + totalBorrowedUSD
    totalReserveUSD = tokenReserveUSD + totalReserveUSD

    print("Asset #", i)
    print(allTokens[i][0])
    print("Token price: ", tokenPrice)
    print("Decimals: ", decimals)
    print("Max LTV: ", maxLtv,"%")
    print("Liquidation threshold: ", liquidationThreshold,"%")
    print("Liquidation penalty: ", liquidationPenalty,"%")
    print("Reserve factor: ", reserveFactor, "%")
    print("Utilization rate: ", utilizationRate, "%")
    print("Avaiable tokens liquidity: ", round(avaiableLiquidity, 2))
    print("Total tokens borrowed: ", round(tokenBorrowed, 2))
    print("Reserve tokens size: ", round(tokenReserve, 2))
    print("Total avaiable USD: ", round(avaiableLiquidityUSD, 2))
    print("Total borrowed USD: ", round(tokenBorrowedUSD, 2))
    print("Total reserve borrowed USD: ", round(tokenReserveUSD, 2))
    print()

    i = i + 1

print("Total Borrows: ", round(totalBorrowedUSD/(10**9), 2), "B")
print("Total Avaiable (TVL): ", round(totalAvaiableLiquidityUSD/(10**9), 2), "B")
print("Total Market Size: ", round(totalReserveUSD/(10**9), 2), "B")