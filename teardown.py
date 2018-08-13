# utils
import datetime



# stellar
from stellar_base.keypair import Keypair
from stellar_base.transaction import Transaction
from stellar_base.builder import Builder
from stellar_base.transaction_envelope import TransactionEnvelope

# auth
from mobius_client_python.auth.challenge import Challenge # Working but has a bug with memo
from mobius_client_python.auth.sign import Sign # working
from mobius_client_python.auth.token import Token # Working
from mobius_client_python.auth.jwt import Jwt # Working

# blockchain
from mobius_client_python.blockchain.account import Account # working
from mobius_client_python.blockchain.account_builder import AccountBuilder # working !
from mobius_client_python.blockchain.add_cosigner import AddCosigner # working
from mobius_client_python.blockchain.create_trustline import CreateTrustline # working
from mobius_client_python.blockchain.friend_bot import FriendBot # working !

# client & app
from mobius_client_python.client import Client # working
from mobius_client_python.app.app import App # working
from mobius_client_python.app.app_builder import AppBuilder # working

from mobius_client_python.utils.keypair import verify # working

# Known bug
#  File "/home/veljko/Documents/PythonSDK/env/lib/python3.5/site-packages/stellar_base/memo.py", line 38, in __init__
#    raise TypeError('Expects string type got a ' + type(text).__name__)
# Won't work with TextMemo(), currently using NoneMemo()

# User/Dev keypair
user_keypair = Keypair.from_seed("SDF6ZKKYYW3PUSOUI7WO2P4ZDFJBG3BCVKOZ7PRKGX7T2ONWC6AUGPZZ")
dev_keypair = Keypair.from_seed("SB3FSSXYPLXG5HXZONRZRUETQAHWHHSU2CDYDA2DCAZYBLRM6FJQ5KIZ")

# Trustline
trust_line_dev = CreateTrustline().call(keypair=dev_keypair)
trust_line_user = CreateTrustline().call(keypair=user_keypair)

# Cosigner
cosig = AddCosigner().call(keypair=user_keypair, cosigner_keypair=dev_keypair)

# App
app = AppBuilder().build(dev_keypair.seed(),user_keypair.address().decode(),network='TESTNET')

client = Client()

mobius = Client().network
mobius = Client().stellar_asset
mobius = Client().horizon_client

asset = client.get_stellar_asset()

print('|  user  |  dev  |')


print(app.user_balance(),app.app_balance(asset))

app.payout(amount=1,asset=asset)

print(app.user_balance(),app.app_balance(asset))

# Challenge
challenge_te_xdr = Challenge(developer_secret=dev_keypair.seed(),
                             expires_in=datetime.datetime.now())\
                             .call()
# Sign
te_xdr = Sign(user_secret=user_keypair.seed(),
              te_xdr=challenge_te_xdr,
              address=dev_keypair.address().decode())\
              .call()
# Token
token = Token(developer_secret=dev_keypair.seed(),
              te_xdr=te_xdr,
              address=user_keypair.address().decode())

# Jwt
jwt = Jwt('Very secure secret')

# encode
jwtoken = jwt.encode(token)
# decode
data = jwt.decode(jwtoken)
