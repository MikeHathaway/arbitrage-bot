import sys
from web3 import Web3, HTTPProvider

from pymaker import Address
from pymaker.deployment import DssDeployment
from pymaker.keys import register_keys
from pymaker.numeric import Wad


# Code retreived from: https://github.com/makerdao/pymaker

web3 = Web3(HTTPProvider(endpoint_uri="https://localhost:8545",
                         request_kwargs={"timeout": 10}))
web3.eth.defaultAccount = sys.argv[1]   # ex: 0x0000000000000000000000000000000aBcdef123
register_keys(web3, [sys.argv[2]])      # ex: key_file=~keys/default-account.json,pass_file=~keys/default-account.pass

mcd = DssDeployment.from_json(web3=web3, conf=open("tests/config/kovan-addresses.json", "r").read())
our_address = Address(web3.eth.defaultAccount)


# Choose the desired collateral; in this case we'll wrap some Eth
collateral = mcd.collaterals['ETH-A']
ilk = collateral.ilk
collateral.gem.deposit(Wad.from_number(3)).transact()

# Add collateral and allocate the desired amount of Dai
collateral.approve(our_address)
collateral.adapter.join(our_address, Wad.from_number(3)).transact()
mcd.vat.frob(ilk, our_address, dink=Wad.from_number(3), dart=Wad.from_number(153)).transact()
print(f"CDP Dai balance before withdrawal: {mcd.vat.dai(our_address)}")

# Mint and withdraw our Dai
mcd.approve_dai(our_address)
mcd.dai_adapter.exit(our_address, Wad.from_number(153)).transact()
print(f"CDP Dai balance after withdrawal:  {mcd.vat.dai(our_address)}")

# Repay (and burn) our Dai
assert mcd.dai_adapter.join(our_address, Wad.from_number(153)).transact()
print(f"CDP Dai balance after repayment:   {mcd.vat.dai(our_address)}")

# Withdraw our collateral
mcd.vat.frob(ilk, our_address, dink=Wad(0), dart=Wad.from_number(-153)).transact()
mcd.vat.frob(ilk, our_address, dink=Wad.from_number(-3), dart=Wad(0)).transact()
collateral.adapter.exit(our_address, Wad.from_number(3)).transact()
print(f"CDP Dai balance w/o collateral:    {mcd.vat.dai(our_address)}")

