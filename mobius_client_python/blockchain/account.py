from stellar_base.keypair import Keypair
from ..client import Client

class Account(object):
    def __init__(self, account, keypair):
        self.account = account
        self.keypair = keypair
        self.asset_issuers = []
        self.client = Client()
        self.client_instance = self.client.get_horizon_client()

    def reload(self):
        try:
            self.account = None
            public_key = self.keypair.address().decode()
            account = self.client_instance.account(address=public_key)
            self.account = account
        except Exception as error:
            return False

        return True

    def trust_line_exsists(self,asset=None):
        if not asset:
            asset = self.client.get_stellar_asset()
        balance = dict(self.find_balance(asset))
        return balance and float(balance['limit']) > 0

    def next_sequence_value(self):
        self.reload()
        account = self.get_info()
        return int(account['sequence']) + 1

    def balance(self,asset=None):
        if not asset:
            asset = self.client.get_stellar_asset()
        return float(self.find_balance(asset)['balance'])

    def get_keypair(self):
        return self.keypair

    def get_info(self):
        return self.account

    def authorized(self,keypair):
        return self.find_signer(public_key=keypair.address().decode())

    def balance_match(self, asset, balance):
        balance = dict(balance) # Bugfix for python 3.5
        if asset.is_native():
            return balance['asset_type'] == 'native'
        else:
            asset_code = balance['asset_code']
            issuer = balance['asset_issuer']
            asset_issuer_addr = Keypair.from_address(asset.issuer).address().decode()
            return asset_code == asset.code and issuer == asset_issuer_addr

    def find_balance(self,asset):
        for item in self.account['balances']:
            if self.balance_match(asset,item) == True:
                return item

    def find_signer(self,public_key):
        for item in self.account['signers']:
            if item['public_key'] == public_key:
                return item
