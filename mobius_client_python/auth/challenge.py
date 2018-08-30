from stellar_base.transaction_envelope import TransactionEnvelope
from stellar_base.operation import Operation, CreateAccount
from stellar_base.transaction import Transaction
from stellar_base.memo import TextMemo,NoneMemo
from stellar_base.keypair import Keypair
from stellar_base.builder import Builder
from stellar_base.asset import Asset

import math
import random
import datetime


# Helper object for timestamps
class Time(object):
    def __init__(self, min_time=0, max_time=0):
        self.minTime = int(min_time)
        self.maxTime = int(max_time)


# Generates challenge transaction on developer's side.
class Challenge(object):
    def __init__(self, developer_secret, expires_in):

        if type(expires_in) is not datetime.datetime:
            raise TypeError('expires_in must be a datetime.datetime object, not a %s' % type(expires_in))

        self.developer_secret = developer_secret
        self.expires_in = expires_in

    def call(self):
        keypair = self.keypair()

        builder = Builder(address=keypair.address().decode(),
                          sequence=self.random_sequence(),
                          secret=keypair.seed())

        builder.sign()

        builder.add_memo(self.memo())
        builder.add_time_bounds(self.build_time_bounds())

        builder.append_payment_op(source=Keypair.random(),
                                  destination=keypair.address().decode(),
                                  amount='0.000001')
        builder.sign()

        te = builder.gen_te()

        return te.xdr()

    def keypair(self):
        return Keypair.from_seed(self.developer_secret)

    def random_sequence(self):
        max_seq_number = 2 ** 128 - 1
        limit = 65535
        return max_seq_number - random.randint(1,limit)

    def build_time_bounds(self):
        min_time = datetime.datetime.now()
        min_time = min_time.timestamp()
        max_time = min_time + self.expires_in.timestamp()
        return Time(min_time,max_time)

    def memo(self):
        # TODO : should return TextMemo('Mobius authentication') but for some reason it throws error.
        return NoneMemo()
