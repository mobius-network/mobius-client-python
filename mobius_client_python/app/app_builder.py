from stellar_base.keypair import Keypair

from ..blockchain.account_builder import AccountBuilder
from .app import App

class AppBuilder(object):
    def build(self, developer_secret, address, network=None):
        dev_keypair = Keypair.from_seed(developer_secret)
        dev_account = AccountBuilder().build(dev_keypair)

        user_keypair = Keypair.from_address(address)
        user_account = AccountBuilder().build(user_keypair)

        return App(dev_account,user_account,network)
