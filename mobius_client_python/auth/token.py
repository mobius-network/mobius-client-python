from stellar_base.transaction_envelope import TransactionEnvelope
from stellar_base.transaction import Transaction
from stellar_base.keypair import Keypair

from ..utils.keypair import verify
from ..client import Client

import datetime
import binascii

class Token(object):
    def __init__(self, developer_secret, te_xdr, address):
        self.developer_secret = developer_secret
        self.te = TransactionEnvelope.from_xdr(te_xdr)
        self.tx = self.te.tx
        self.address = address
        self.keypair = self.keypair()
        self.user_keypair = self.user_keypair()
        self.time_bounds()
        
    def time_bounds(self):
        self.bounds = self.tx.time_bounds

        if not self.bounds:
            raise Exception("Malformed Transaction")

        return self.bounds

    def hash(self, format='binary'):
        self.validate()

        hash_meta = self.te.hash_meta()
        if format == 'binary':
            return hash_meta

        return binascii.hexlify(hash_meta).decode()

    def envelope(self, xdr):
        return TransactionEnvelope.from_xdr(xdr)

    def validate(self, strict=True):
        if not self.signed_correctly():
            raise Exception('Wrong challenge transaction signature')

        bounds = self.time_bounds()

        if self.time_now_covers(bounds):
            raise Exception('Challenge transaction expired')

        if strict and self.too_old(bounds):
            raise Exception('Challenge transaction expired')

        return True

    def keypair(self):
        return Keypair.from_seed(self.developer_secret)

    def user_keypair(self):
        return Keypair.from_address(self.address)

    def signed_correctly(self):
        signed_by_dev = verify(self.te,self.keypair)
        signed_by_user = verify(self.te,self.user_keypair)
        return signed_by_dev and signed_by_user

    def time_now_covers(self,time_bounds):
        min_time = time_bounds[0].minTime
        max_time = time_bounds[0].maxTime
        now = datetime.datetime.now().timestamp()

        if min_time > now and max_time < now:
            return True
        else:
            return False

    def too_old(self,time_bounds):
        min_time = time_bounds[0].minTime
        now = datetime.datetime.now() - datetime.timedelta(seconds=Client.strict_interval)
        now = now.timestamp()
        return now > min_time
