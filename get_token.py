import requests

base_url = "http://localhost:5000/api/"

friend_bot_url = "https://mobius.network/friendbot"

xdr = requests.get(base_url)

token = requests.post(base_url,json={"xdr":xdr.text})
token = str(token.text)

f = open('token.txt', 'w')

f.write(token)

f.close()
