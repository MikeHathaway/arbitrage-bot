from web3 import Web3, HTTPProvider

class ConnectedWallet:
    
    def __init__(self, node: string):
        self.web3 = Web3(HTTPProvider(node))

    @staticmethod
    def get_contract(abi: list, address: Address):
        pass 

ConnectedWallet('http://127.0.0.1:8545')
