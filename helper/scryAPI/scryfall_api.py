import requests
from requests import Session
import secrets
import json
import time
from pprint import pprint as pp


# no need, public API that can be used without an auth key.
# user_info = "settings.json"


# scryfall API works now, still need to make the changes here.
# Will continue to have an issue with promo cards.
class scryAPI:
    
    def __init__(self, token = ''):
        self.scryURL = "https://api.scryfall.com/"
        self.header = {}
        self.session = Session()
        self.token = token
        
    def getCollectionData(self, ids, id_type = ['collector_number','set'], query = False, verbose = False):
        # list of ids from the df to eventually join back on
        
        url = self.scryURL + "cards/collection/"
        data = []
        divisor = ids.shape[0] // 75
        missing = []
        
        if verbose:
            print(f'First four ids: {ids[:4]}',
                  f'Divisor is: {divisor}',
                  f'id_type is: {id_type}',
                  f'query set to: {query}',
                  sep = '\n')
        
        # we need to ensure that we are being polite with our API requests
        # scryfall requests you put 50-100ms delay, or do not average more than
        # 10 requests per second.
        # This should do ~1k cards in a little under 30 seconds.
        
        # There should be a saved list of the keys that you can query that are
        # checked before you actually get to pull the information. Alternately
        # check the docs for if there is a way to just pull specific information
        # so we are more curtious with our queries.
        
        
        # I wrote this wrong originally, query should be handled by a different function
        # or at the end of processing since we cannot return data in a meaningful way
        # 
        ids.columns = id_type
        
        if 'collector_number' in id_type:
            ids.collector_number = ids.collector_number.astype(str)
        
        ids = ids.loc[::,['set', 'collector_number']]
        
        while divisor > 0:
            current_ids = ids.iloc[:75,::]
            ids = ids.iloc[75:,::]
            
            if verbose:
                print(f'Length of current_ids: {current_ids.shape[0]}',
                      f'Length of ids: {ids.shape[0]}',
                      f'Missing IDS so far: {missing}',
                      #f'Column order: {current_ids.columns}',
                      sep = '\n')
            
            parameters = {
                'identifiers' : list(current_ids.to_dict(orient = 'index').values())
            }
            if query:
                r = self.session.post(url, json=parameters)
                data.extend(r.json()['data'].get(query, 'Category Not Found'))
                missing.extend(r.json().get('not_found', ''))
            else:
                r = self.session.post(url, json=parameters)
                data.extend(r.json()['data'])
                missing.extend(r.json().get('not_found', ''))
                
            
            divisor -= 1
            time.sleep(2)
        
        parameters = {
            'identifiers' : list(ids.to_dict(orient = 'index').values())
        }
        
        if query:
            r = self.session.post(url, json = parameters)
            data.extend(r.json()['data'])
            missing.extend(r.json().get('not_found', ''))

        else:
            r = self.session.post(url, json = parameters)
            if verbose:
                print(f'Parameters : {parameters}')
                # print('API post output', sep = ": ")
                # pp(r.json()['data'])
            data.extend(r.json()['data'])
            missing.extend(r.json().get('not_found', ''))

        if verbose:
            pp(missing)
        return data