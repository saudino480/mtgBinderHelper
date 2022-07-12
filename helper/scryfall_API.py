import requests
from requests import Session
import secrets
import json
import time

# no need, public API that can be used without an auth key.
# user_info = "settings.json"


# scryfall API works now, still need to make the changes here.
# Will continue to have an issue with promo cards.
class scryAPI:
    
    def __init__(self, token):
        self.scryURL = "https://api.scryfall.com/"
        self.header = {}
        self.session = Session()
        self.token = token
        
    def getCollectionData(self, multiverse_ids):
        url = self.scryURL + "cards/collection/"
        data = []
        divisor = len(multiverse_ids) // 75
        header = {'Content-Type' : "application/json"}
        self.session.header.update(header)
        
        # we need to ensure that we are being polite with our API requests
        # scryfall requests you put 50-100ms delay, or do not average more than
        # 10 requests per second.
        # This should do ~1k cards in a little under 30 seconds.
        while divisor > 0:
            current_ids = multiverse_ids[:75]
            multiverse_ids = multiverse_ids[75:]
            
            # this needs to be a list of jsons
            parameters = {
                'identifiers' : [{'multiverse_id': idx} for idx in current_ids]
            }
            
            r = self.session.get(url, params=parameters)
            data = data.append(r.json())
            
            divisor -= 1
            time.sleep(2)
        
        parameters = {
            'identifiers' : [{'multiverse_id': idx} for idx in multiverse_ids]
        }
        
        r = self.session.get(url, params = parameters)
        data = data.append(r.json())
        
        return data
        
