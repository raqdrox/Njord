import requests
import json

def getTokens():
    authCodes=None

    with open('./tokens/SLauth.json','r') as f:
        authCodes=json.load(f)

    data = {
    'grant_type': 'authorization_code',
    'client_id':  authCodes['client_id'],
    'client_secret': authCodes['client_secret'],
    'redirect_uri': authCodes['redirect_uri'],
    'code': authCodes['code']
    }

    resp = requests.post('https://streamlabs.com/api/v1.0/token', data=data)
    response = resp.json()

    if 'error' not in response.keys():
        authCodes['access_token']=response['access_token']
        authCodes['refresh_token']=response['refresh_token']
    else:
        print(response['error'])
        return 0



    with open('./tokens/SLauth.json','w') as f:
        json.dump(authCodes,f,indent=4)

    return authCodes['access_token']

def refreshTokens():
    with open('./tokens/SLauth.json','r') as f:
        authCodes=json.load(f)

    data = {
    'grant_type': 'refresh_token',
    "refresh_token": authCodes['refresh_token'],
    'client_id':  authCodes['client_id'],
    'client_secret': authCodes['client_secret'],
    'redirect_uri': authCodes['redirect_uri']
    }
    resp = requests.post('https://www.twitchalerts.com/api/v1.0/token', data=data)
    
    response = resp.json()
    if 'error' not in response.keys():
        authCodes['access_token']=response['access_token']
        authCodes['refresh_token']=response['refresh_token']
    else:
        print(response['error'])
        


    with open('./tokens/SLauth.json','w') as f:
        json.dump(authCodes,f,indent=4)

    return authCodes['access_token']

def postDonations(donation,token):
    if len(donation['name'])>24:
        donation['name']=donation['name'][:23]
    data = {
    "name":donation['name'],
    "message":donation['message'],
    "identifier":'None',
    "amount":donation['amount'],
    "currency":"INR",
    "access_token":token
    }
    response = requests.request("POST", "https://streamlabs.com/api/v1.0/donations", data=data)
    print(response.text)
