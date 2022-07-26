import requests
from requests import Session
import secrets
import json
from helper import helper as h

# user_info = "settings.json"
             
class echoMTGAPI:
    
    # used to grab cards from online, with pricing
    
    def __init__(self, user_info):
        self.api_url = 'https://www.echomtg.com/api/'
        self.session = Session()
        
        # there is a chance you have to refresh your token
        # so we do that and generate a new token (will just be the same)
        # if the token doesn't need to be refreshed.
        def getToken(user_info):
            settings = json.load(open(user_info))['echoMTG']
            r = requests.post(self.api_url + "user/auth/", data={'email':settings['email'],
                                                  'password': settings['password']})
            print(r.text)
            responseBody = json.loads(r.text)
            if responseBody['status'] == 'success':
                return responseBody['token']
            else:
                print('Token not returned! Please recheck your user settings and then try to run the application again.')
                return 'Invalid Token'
        self.token = getToken(user_info)
        
    # these are the cards we own
    def inventoryDump(self):
        url = self.api_url + "inventory/dump/" + "auth=" + self.token
        r = self.session.get(url)
        data = r.json()['inventoryData']
        return data
    
    # we will use this to connect with Scryfall for pricing data
    def cardReference(self):
        url = self.api_url + "data/card_reference/auth=" + self.token
        r = self.session.get(url)
        data = r.json()['cards']
        return data

    
    def fullDataDump(self):
        
        inventory = self.inventoryDump()
        reference = self.cardReference()
        
        combined_info = h.collator(inventory, reference)
        
        cleaned_info = h.name_handler(combined_info, 'name')
        cleaned_info.set_code = cleaned_info.set_code.str.upper()
        cleaned_info.fillna('', inplace=True)
        
        return cleaned_info
        