from stellar_base.builder import Builder
from stellar_base.operation import Payment

from ..client import Client

class App(object):
    def __init__(self, app_account, user_account, network=None):
        self.app_account = app_account
        self.user_account = user_account
        self.network = network
        self.client_instance = Client(network).get_horizon_client()

    def authorized(self):
        return self.user_account.authorized(self.app_keypair())

    def app_account(self):
        return self.app_account

    def app_balance(self,asset):
        return self.app_account.balance(asset)

    def app_keypair(self):
        keypair = self.app_account.get_keypair()
        if not keypair:
            keypair = self.user_account.keypair
        return keypair

    def user_account(self):
        return self.user_account.get_keypair()

    def user_balance(self):
        self.validate_user_balance()

        return self.user_account.balance()

    def user_keypair(self):
        keypair = self.user_account.get_keypair()
        if not keypair:
            keypair = self.user_account.keypair
        return keypair

    def charge(self, amount, destination=None):
        if self.user_balance() < float(amount):
            raise Exception('Insufficient Funds')

        te = self.build_te()

        if destination:
            te.tx.add_operation(self.app_payment_op(amount,destination))
        else:
            te.tx.add_operation(self.user_payment_op(amount,self.app_keypair().address().decode()))

        te.sign(self.app_keypair())

        self.submit_tx(te)

        return te

    def payout(self, amount, asset, destination=None):

        if not destination:
            destination = self.user_keypair().address().decode()

        if self.app_balance(asset) < float(amount):
            raise Exception('Insufficient Funds')

        te = self.build_te()

        te.tx.add_operation(self.app_payment_op(amount,destination))

        te.sign(self.app_keypair())

        self.submit_tx(te)

        return te

    def transfer(self, amount, destination):
        if self.user_balance() < float(amount):
            raise Exception('Insufficient Funds')

        te = self.build_te()

        te.tx.add_operation(self.user_payment_op(amount,destination))

        te.sign(self.app_keypair())

        self.submit_tx(te)

        return te

    def build_te(self):
        builder = Builder(address=self.user_account.get_info()['account_id'])
        te = builder.gen_te()

        return te


    def submit_tx(self, te):

        response = self.client_instance.submit(te.xdr().decode())

        self.reload()

        return te

    def reload(self):
        return self.app_account.reload() and self.user_account.reload()


    def user_payment_op(self, amount, destination):
        return Payment(opts={'destination': destination,
                             'amount': str(amount),
                             'asset': Client(self.network).get_stellar_asset(),
                             'source': self.user_keypair().address().decode()
                             })

    def app_payment_op(self, amount, destination):
        return Payment(opts={'destination': destination,
                             'amount': str(amount),
                             'asset': Client(self.network).get_stellar_asset(),
                             'source': self.app_keypair().address().decode()
                            })

    def validate_user_balance(self):
        if not self.authorized():
            raise Exception('Authorisation missing')

        if not self.user_account.trust_line_exsists():
            raise Exception('Trustline not found')
