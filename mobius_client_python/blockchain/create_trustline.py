from stellar_base.transaction_envelope import TransactionEnvelope
from stellar_base.builder import Builder
from stellar_base.transaction import ChangeTrust

from ..client import Client
from .account_builder import AccountBuilder

class CreateTrustline(object):
    def call(self, keypair, asset=Client().get_stellar_asset()):
        client = Client().get_horizon_client()
        account = AccountBuilder().build(keypair)
        te = self.tx(account.get_info(),asset)

        te.sign(keypair)

        return client.submit(te.xdr())

    def tx(self, account, asset):
        builder = Builder(address=account['account_id'])

        builder.append_op(ChangeTrust(opts={'asset':asset}))

        return builder.gen_te()
