import echoMTG_api as echoAPI
import json
from pprint import pprint as pp
import csv
import os
import io

user_info = "helper/settings.json"

eMTG = echoAPI.echoMTGAPI(user_info)

if not os.path.exists('./data/cardReference.json'):
    print("Skipping Card Reference Download")
    pass
else:
    all_cards = eMTG.cardReference()
    with io.open('./data/cardReference.json', 'w', encoding='utf-8') as outputfile:
        outputfile.write(json.dumps(all_cards, ensure_ascii=False))
        

inventory = eMTG.inventoryDump()

with io.open('./data/inventory_unprocessed.json', 'w', encoding='utf-8') as outputfile:
    outputfile.write(json.dumps(inventory, ensure_ascii=False))
    


