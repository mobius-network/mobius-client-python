from stellar_base.transaction_envelope import TransactionEnvelope
from stellar_base.transaction import Transaction
from stellar_base.keypair import Keypair
from stellar_base.builder import Builder

from ..utils.keypair import verify

# Signs challenge transaction on user's side.
class Sign(object):
    def __init__(self, user_secret, te_xdr, address):
        self.user_secret = user_secret # seed
        self.xdr = te_xdr # 'TransactionEnvelope' object xdr
        self.address = address # Developer public key

    def call(self):
        te = TransactionEnvelope.from_xdr(xdr=self.xdr)
        keypair = self.keypair()
        dev_keypair = self.dev_keypair()
        self.validate(dev_keypair,te)

        te.sign(keypair)

        return te.xdr().decode()

    def keypair(self):
        return Keypair.from_seed(self.user_secret)

    def dev_keypair(self):
        return Keypair.from_address(self.address)

    def validate(self, keypair, te):
        is_valid = verify(te,keypair)
        if is_valid == False:
            raise Exception("Wrong challenge transaction signature")
        else:
            return True
