from stellar_base.asset import Asset
from stellar_base.network import Network, NETWORKS
from stellar_base.horizon import Horizon

issuers = {
    'PUBLIC':'GA6HCMBLTZS5VYYBCATRBRZ3BZJMAFUDKYYF6AH6MVCMGWMRDNSWJPIH',
    'TESTNET':'GDRWBLJURXUKM4RWDZDTPJNX6XBYFO3PSE4H4GPUL6H6RCUQVKTSD4AT'
}
urls = {
  'TESTNET': 'https://horizon-testnet.stellar.org',
  'PUBLIC': 'https://horizon.stellar.org'
}


class Client(object):

    asset_code = 'MOBI'
    challenge_expires_in = 60 * 60 * 24
    mobius_host = 'https://mobius.network'
    strict_interval = 10

    def __init__(self, network=None):
        self.stellar_asset = None
        self.horizon_client = None
        if network == None or network == 'TESTNET':
            self.network = Network(NETWORKS['TESTNET'])
        else:
            self.network = Network(NETWORKS['PUBLIC'])
        # Run
        self.stellar_asset = self.get_stellar_asset()
        self.horizon_client = self.get_horizon_client()

    def get_network(self):
        return self.network

    def get_asset_issuer(self):
        if self.network.network_id == NETWORKS['PUBLIC']:
            return issuers['PUBLIC']
        else:
            return issuers['TESTNET']

    def get_stellar_asset(self):

        if self.stellar_asset:
            return self.stellar_asset

        stellar_asset = Asset(self.asset_code,self.get_asset_issuer())
        self.stellar_asset = stellar_asset

        return self.stellar_asset

    def get_horizon_client(self):
        if self.horizon_client:
            return self.horizon_client

        network_passphrase = self.network.network_id()

        if network_passphrase == NETWORKS['PUBLIC']:
            horizon_client = Horizon(urls['PUBLIC'])
        else:
            horizon_client = Horizon(urls['TESTNET'])

        self.horizon_client = horizon_client

        return self.horizon_client
