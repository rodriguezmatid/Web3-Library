from web3 import Web3
import json
import dotenv as _dotenv
import os as os
from requests import Session

_dotenv.load_dotenv()

# ##########################
# ###### Mainnet ###########
# ##########################
rpc = 'https://polygon-rpc.com'
# infura_url = os.environ["INFURA_URL"]
web3 = Web3(Web3.HTTPProvider(rpc))

addressProtocolDataProvider = web3.toChecksumAddress('0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654')
addressPriceOracle = web3.toChecksumAddress('0xb023e699F5a33916Ea823A16485e259257cA8Bd1')

if web3.isConnected() == True:
    print('Logged in')
else:
    print('Not logged')

with open('./utils/protocolDataProviderV3.json', 'r') as f:
    abi_protocolDataProvider = json.load(f)

with open('./utils/priceOracleV3.json', 'r') as f:
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

contractProtocolDataProvider = web3.eth.contract(address = addressProtocolDataProvider, abi = abi_protocolDataProvider)
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
    print("Total borrowed USD: ", "{:,.2f}".format(tokenBorrowedUSD))
    print("Total reserve borrowed USD: ", round(tokenReserveUSD, 2))
    print()

    i = i + 1

print("Total Borrows: ", "{:,.2f}".format(totalBorrowedUSD/(10**9)), "B")
print("Total Avaiable (TVL): ", round(totalAvaiableLiquidityUSD/(10**9), 2), "B")
print("Total Market Size: ", round(totalReserveUSD/(10**9), 2), "B")