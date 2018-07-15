from .account import Account
from ..client import Client

class AccountBuilder(object):
    def build(self, keypair):
        account_id = keypair.address().decode()
        account = Client().horizon_client.account(address=account_id)
        return Account(account,keypair)
