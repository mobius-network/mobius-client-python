import jwt

class Jwt(object):
    def __init__(self,secret):
        self.ALG = 'HS512'
        self.secret = secret

    def encode(self, token):
        payload = {
            'hash': token.hash('hex'),
            'public_key': token.address,
            'min_time': token.bounds[0].minTime,
            'max_time': token.bounds[0].maxTime,
        }

        return jwt.encode(payload,self.secret,self.ALG)

    def decode(self, value):
        return jwt.decode(value,self.secret,algorithms=[self.ALG])
