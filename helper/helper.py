import os
import pandas as pd
import json


# this takes the two echoMTG dfs and combines them
def collator(inventory, cardReference):
    
    # name formatting
    clean_names = {'i' : "ID",
               'e' : "echo_id",
               't' : 'tradable',
               'f' : 'foil',
               'p' : 'price',
               'a' : 'date_acq',
               'c' : 'date_db_added',
               'u' : 'date_updated',
               'd' : 'date_deleted'}
    
    inv_df = pd.DataFrame(inventory)
    inv_df = inv_df.rename(clean_names, axis = 1)
    
    card_df = pd.DataFrame.from_dict(cardReference, orient = 'index')
    
    inv_df_aug = inv_df.merge(card_df, how = "left", on = "echo_id")
    
    return inv_df_aug


def name_handler(df, col_name):
    # names include treatment types, and so the 
    split_list = df[col_name].str.split(" \(", n=1)
    name_list = [name[0] for name in split_list]
    
    temp_df = df.copy()
    temp_df[col_name] = name_list
    temp_df['treatment'] = [name[1] if len(name) > 1 else "" for name in split_list]
    temp_df['treatment'] = temp_df['treatment'].str.replace("\)", "")
    
    return temp_df