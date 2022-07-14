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
        
    def getCollectionData(self, ids, id_type = ['set_code', 'number']):
        # list of ids from the df to eventually join back on
        # 
        
        url = self.scryURL + "cards/collection/"
        data = []
        divisor = len(multiverse_ids) // 75
        
        # we need to ensure that we are being polite with our API requests
        # scryfall requests you put 50-100ms delay, or do not average more than
        # 10 requests per second.
        # This should do ~1k cards in a little under 30 seconds.
        
        # There should be a saved list of the keys that you can query that are
        # checked before you actually get to pull the information. Alternately
        # check the docs for if there is a way to just pull specific information
        # so we are more curtious with our queries.
        while divisor > 0:
            current_ids = multiverse_ids[:75]
            multiverse_ids = multiverse_ids[75:]
            
            parameters = {
                'identifiers' : [{'multiverse_id': idx} for idx in current_ids]
            }
            if query:
                r = self.session.get(url, params=parameters)
                data = data.append(r.json()['data'][0].get(query, 'Category Not Found'))
            else:
                r = self.session.get(url, params=parameters)
                data = data.append(r.json()['data'][0])
            
            divisor -= 1
            time.sleep(2)
        
        parameters = {
            'identifiers' : [{'multiverse_id': idx} for idx in multiverse_ids]
        }
        if query:
            r = self.session.get(url, params = parameters)
            data = data.append(r.json()['data'][0][query])
        else:
            r = self.session.get(url, params = parameters)
            data = data.append(r.json()['data'][0])
        return data
        
