import requests

class FriendBot(object):
    def call(self,keypair):
        public_key = keypair.address().decode()
        url = 'https://horizon-testnet.stellar.org/friendbot'
        r = requests.get(url,params={'addr':public_key})
        return r.json()
