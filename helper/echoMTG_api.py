import requests
from requests import Session
import secrets
import json
from pprint import pprint as pp

user_info = "settings.json"

def getToken(settings = json.load(open(user_info)):
    r = requests.post(self.api_url, data={'email':settings['email'],
                                          'password': settings['password']})
    responseBody = json.loads(r.text)
    if responseBody['status'] == 'success':
        return responseBody['token']
             

class echoMTGAPI:
    
    def __init__(self, user_info):
        self.api_url = 'https://www.echomtg.com/api/'
        self.session = Session()
        # cannot use the headers = self.headers here, since there is a secret splat
        def getToken(settings = json.load(open(user_info))):
            r = requests.post(self.api_url, data={'email':settings['email'],
                                                  'password': settings['password']})
            responseBody = json.loads(r.text)
            if responseBody['status'] == 'success':
                return responseBody['token']
            else:
                print('Token not returned! Please recheck your user settings and then try to run the application again.')
                return 'Invalid Token'
        self.token = getToken()
        

    def inventoryDump(self):
        url = self.api_url + "inventory/dump/" + "auth=" + self.token
        r = self.session.get(url)
        data = r.json()
        column_headers = data['headerMap']
        data = data['inventoryData']
        return data, column_headers
    
    def cardReference(self):
        url = self.api_url + "data/card_reference/auth=" + self.token
        r = self.session.get(url)
        data = r.json()['cards']
        return data
        
    