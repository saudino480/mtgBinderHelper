import requests
from requests import Session
import secrets
import json
import time

# no need, public API that can be used without an auth key.
# user_info = "settings.json"


class scryAPI:
    
    def __init__(self, token):
        self.scryURL = "https://api.scryfall.com/"
        self.header = {}
        self.session = Session()
        
    def getCollectionData(self, multiverse_ids):
        url = self.scryURL + "cards/collection/"
        data = []
        divisor = len(multiverse_ids) // 75
        
        # we need to ensure that we are being polite with our API requests
        # scryfall requests you put 50-100ms delay, or do not average more than
        # 10 requests per second.
        # This should do ~1k cards in a little under 30 seconds.
        while divisor > 0:
            current_ids = multiverse_ids[:75]
            multiverse_ids = multiverse_ids[75:]
            
            parameters = {
                'multiverse_id' : current_ids
            }
            
            r = self.session.get(url, params=parameters)
            data = data.append(r.json())
            
            divisor -= 1
            time.sleep(2)
        
        parameters = {
            'multiverse_id' : multiverse_ids
        }
        
        r = self.session.get(url, params = parameters)
        data = data.append(r.json())
        
        return data
        
