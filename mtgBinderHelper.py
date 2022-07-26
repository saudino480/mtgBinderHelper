import requests
from requests import Session
import helper/secrets
import json
import helper/echoMTG_api as echoMTG
import helper/scryfall_api as scryfall
import helper/helper as h
import pandas as pd
import time

# Connect to the echoMTG website that holds the binder information
echoClient = echoMTG.echoMTGAPI('helper/settings.json')
inventoryDB = echoClient.fullDataDump()
inventoryDB.set_code = inventoryDB.set_code.str.upper()
referenceJSON = json.load(open("data/AllPrintings.json"))

# preprocessing + data cleaning
combined_inventoryDB = h.set_up(inventoryDB, referenceJSON, verbose = False)

# will probably get rolled into other functions, but need to clean up these first
clean_inventoryDB['promo'] = clean_inventoryDB.expansion.str.contains('Promo Pack', case = False)
clean_inventoryDB['expansion'] = clean_inventoryDB.expansion.str.replace("Promo Pack: ", "")
clean_inventoryDB['set_code'] = clean_inventoryDB[['set_code', 'promo']].apply(lambda card: h.promo_helper(card.set_code, card.promo), axis = 1)

# get unique ids for set codes so we don't have to ask Scryfall's website for it multiple times
ids = clean_inventoryDB[['set_number', 'set_code']].drop_duplicates()

# finally hooking into the API, dumping the data.
sfClient = scryfall.scryAPI('na')
output = sfAPI.getCollectionData(ids, verbose = False)

# 
outputDB = pd.DataFrame(output)
price_list = outputDB.loc[::,['name', 'set', 'collector_number', 'prices']]
price_list.set = price_list.set.str.upper()
price_list.collector_number = price_list.collector_number.astype(int)

clean_inventoryDB.foil = clean_inventoryDB.foil.astype(int)
completed_inventory = clean_inventoryDB.apply(lambda card: h.price_lookup(card, price_list, verbose = False), axis = 1)

outputDB.to_csv("../data/scryfallDB.csv")
completed_inventory.to_csv("../data/cleaned_inventory.csv")