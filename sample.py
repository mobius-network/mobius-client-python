from flask import Flask
from flask_cors import CORS
from flask import jsonify

from mobius_client_python.auth.challenge import Challenge
from mobius_client_python.auth.token import Token

from stellar_base.keypair import Keypair

# Flask app
app = Flask(__name__)

# Enable cors
CORS(app)

dev_keypair = Keypair.random()

@app.route('/auth', methods=('GET', 'POST'))
def auth():
    if request.method == 'GET':
        """
        GET /auth
        Generates and returns challenge transaction XDR signed by application to user
        """
        xdr = Challenge(developer_secret=dev_keypair.seed(), # Developer SECRET_KEY
                                     expires_in=datetime.datetime.now())\
                                     .call()
        response = {'xdr': xdr}
    elif request.method == 'POST':
        """
        POST /auth
        Validates challenge transaction. It must be:
        Signed by application and requesting user.
        Not older than 10 seconds from now (see mobius_client_python.client.Client.strict_interval)
        """
        try:
            te_xdr = request.form['te_xdr']
            address = request.form['public_key']
            token = Token(developer_secret=dev_keypair.seed(),
                        te_xdr=te_xdr,
                        address=address)
            token.validate()
            response = {'token':token.hash('hex')}
        except Exception as e:
            response = {'error':e}
    return jsonify(response)
