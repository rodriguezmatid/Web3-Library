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


LendingPoolAddressesProvider = web3.toChecksumAddress('0xb53c1a33016b2dc2ff3653530bff1848a515c8c5')
lendingPoolAddressesProviderRegistry = web3.toChecksumAddress('0x52D306e36E3B6B02c153d0266ff0f85d18BCD413')
lendingPool = web3.toChecksumAddress('0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9')
LendingPoolCollateralManager = web3.toChecksumAddress('0xbd4765210d4167ce2a5b87280d9e8ee316d5ec7c')
LendingPoolConfigurator = web3.toChecksumAddress('0x311bb771e4f8952e6da169b425e7e92d6ac45756')
LendingRateOracle = web3.toChecksumAddress('0x8a32f49ffba88aba6eff96f45d8bd1d4b3f35c7d')
PriceOracle = web3.toChecksumAddress('0xa50ba011c48153de246e5192c8f9258a2ba79ca9')
PoolAdmin = web3.toChecksumAddress('0xee56e2b3d491590b5b31738cc34d5232f378a8d5')
EmergencyAdmin = web3.toChecksumAddress('0xca76ebd8617a03126b6fb84f9b1c1a0fb71c2633')
protocolDataProvider = web3.toChecksumAddress('0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d')
WETHGateway = web3.toChecksumAddress('0xEFFC18fC3b7eb8E676dac549E0c693ad50D1Ce31')
AaveCollector = web3.toChecksumAddress('0x464c71f6c2f760dda6093dcb91c24c39e5d6e18c')
IncentivesController = web3.toChecksumAddress('0xd784927Ff2f95ba542BfC824c8a8a98F3495f6b5')
UiPoolDataProvider = web3.toChecksumAddress('0x30375522F67a6308630d49A694ca1491fA2D3BC6')
UiIncentiveDataProvider = web3.toChecksumAddress('0xD01ab9a6577E1D84F142e44D49380e23A340387d')

contractProtocolDataProvider = web3.eth.contract(address = protocolDataProvider, abi = abi_protocolDataProvider)
contractLendingPool = web3.eth.contract(address = lendingPool, abi = abi_lendingPool)
contractLendingPoolAddressesProviderRegistry = web3.eth.contract(address = lendingPoolAddressesProviderRegistry, abi = abi_lendingPoolAddressesProviderRegistry)

#token = contractProtocolDataProvider.functions.getAllReservesTokens().call()
lending = contractLendingPoolAddressesProviderRegistry.functions.getAddressesProvidersList().call()
#tokenBalance = contractProtocolDataProvider.functions.getReserveConfigurationData('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48').call()
#tokenBalance1 = contractProtocolDataProvider.functions.getReserveData('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48').call()
#tokenBalance1 = to
print(lending)
