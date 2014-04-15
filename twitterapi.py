# Encoding: UTF-8

import urllib
import base64
import pprint

import requests
from requests.auth import AuthBase

# z https://apps.twitter.com/
# (access_token doplnit po prvním přihlášení)
from kody import api_key, api_secret, access_token


def get_access_token():
    # viz https://dev.twitter.com/docs/auth/application-only-auth
    secret = urllib.quote(api_key) + ':' + urllib.quote(api_secret)
    secret64 = base64.b64encode(secret)

    headers = {
        'Authorization': 'Basic ' + secret64,
        'Host': 'api.twitter.com',
    }
    response = requests.post('https://api.twitter.com/oauth2/token',
                            headers=headers,
                            data={'grant_type': u'client_credentials'})

    print 'Dotaz:'
    print response.request.headers
    print response.request.body

    print 'Odpověď:'
    print response.headers
    print response.text

    return response.json()['access_token']

if not access_token:
    access_token = get_access_token()

def bearer_auth(request):
    request.headers['Authorization'] = 'Bearer ' + access_token
    return request

session = requests.Session()
session.auth = bearer_auth

response = session.get(
    'https://api.twitter.com/1.1/search/tweets.json',
    params={'q': '#vesmír'},
)
response.raise_for_status()
data = response.json()

#pprint.pprint(data)

pprint.pprint(dict(response.headers))

for tweet in data['statuses']:
    print tweet['id_str']
    print tweet['text']

