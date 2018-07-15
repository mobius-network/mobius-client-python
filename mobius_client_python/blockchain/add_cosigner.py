from stellar_base.transaction_envelope import TransactionEnvelope
from stellar_base.transaction import Transaction
from stellar_base.operation import SetOptions
from stellar_base.builder import Builder

from .account_builder import AccountBuilder
from ..client import Client


class AddCosigner(object):

    def call(self, keypair, cosigner_keypair, weight=1):
        client = Client().get_horizon_client()
        account = AccountBuilder().build(keypair)
        te = self.tx(account,cosigner_keypair,weight)

        te.sign(keypair)

        return client.submit(te.xdr())

    def tx(self, account, cosigner_keypair, weight):

        builder = Builder(address=account.get_info()['account_id'])

        builder.append_set_options_op(
            high_threshold=10,
            low_threshold=1,
            master_weight=10,
            med_threshold=1,
            signer_weight=weight,
            signer_address=cosigner_keypair.address().decode(),
            signer_type='ed25519PublicKey')

        return builder.gen_te()
