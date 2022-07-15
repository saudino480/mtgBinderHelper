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


def name_handler(df, col_name, split_on = " \("):
    # names include treatment types, and so the 
    split_list = df[col_name].str.split(split_on, n=1)
    name_list = [name[0] for name in split_list]
    
    temp_df = df.copy()
    temp_df[col_name] = name_list
    temp_df['treatment'] = [name[1] if len(name) > 1 else "" for name in split_list]
    temp_df['treatment'] = temp_df['treatment'].str.replace("\)", "", regex=True)
    
    return temp_df

# main methods

def set_up(data, referenceJSON, verbose = False):
    
    sets_to_check = [sets for sets in data.set_code.unique() if sets not in ['PPRE', 'BAB']]

    referenceDB = pd.DataFrame()

    for sets in sets_to_check:
        single_setDB = pd.DataFrame(referenceJSON['data'][sets]['cards'])
        referenceDB = referenceDB.append(single_setDB)

    # we will not be looking at tokens, so we must remove them
    data = data[~data.treatment.str.contains('token',case=False)]
    data_by_set = data.groupby('set_code')

    results = pd.DataFrame(columns = data.columns)

    for set_code, set_df in data_by_set:
        if set_code not in ['PPRE', 'BAB']:
            set_referenceDB = referenceDB[referenceDB.setCode == set_code]
        else:
            set_referenceDB = referenceDB
        
        if verbose:
            print('%'*50, f'Processing Set: {set_code}', sep = '\n')
            print(f'Shape of results: {results.shape[0]}')
            print(f'Shape of referenceDB after filtering by set: {set_referenceDB.shape}')

        set_df['set_number'] = set_df.apply(lambda card: fetch_setnumber(card, set_referenceDB, verbose=verbose), axis = 1)
    
        results = results.append(set_df)
        
        if verbose:
            print(f'Done with {set_code}.', '%'*50, sep = '\n')
    
    results.set_number = results.set_number.astype(int)
    results.foil = results.foil.astype(int)

    return results

def lookup(name, relevant_keys, referenceDB, promo_flag = False, sta_flag = False, verbose = False):
    '''
    Documentation TBA
    Looks up the cards. Returns the results. Handles set goofiness as well.
    Takes:
    name: str
    relevant_keys: list of length two
    referenceDB: pd.DataFrame containing card reference information
    promo_flag: Bool Is it a promo?
    sta_flag: Bool Is it from Strixhaven: Mystical Archive?
    verbose: Bool Flag to turn diagnostic messages on/off
    
    returns:
    result: single row of a df containing the full information from our refrenceDB
            of the card we looked up
            
    
    '''
    
    filtered = referenceDB[referenceDB.name == name]
    
    if filtered.shape[0] == 0:
        filtered = referenceDB[referenceDB.name.str.contains(name)]
        
        if filtered.shape[0] == 0:
            filtered = referenceDB[referenceDB.name.str.lower() == name.lower()]
    
    filtered.number = filtered.number.str.replace("[^0-9]", "", regex = True).astype(int)
    
    if verbose:
        print("*"*4)
        print("In lookup")
        print(f"Name: {name}", 
              f"Relevant Keys: {relevant_keys}", 
              f"Promo Flag: {promo_flag}", 
              f"Strixhaven Mystical Archive Flag: {sta_flag}",
              f"DB View: \n{filtered.loc[::,['name', 'number', relevant_keys[0]]]}",
              f"result: {any(filtered.isPromo)}",
              sep = '\n')
    
    # extended art cards need to be handled in the very specific situation where the
    # buy-a-box promo is also that card. Buy-a-box will typically be the highest
    # numbered card in the set.
    #print(f"result: {any(filtered.isPromo)}")
    
    if relevant_keys[1] == '':
        
        result = filtered.iloc[0]
    
    elif relevant_keys[1] == 'extended art':
        
        result = filtered.iloc[-1]
        
    elif relevant_keys[1] == ['showcase']:
        
        if filtered.setCode.iloc[0] != 'SNC':
            result = filtered.iloc[-1]
        else:
            result = filtered.iloc[-2]
        
    elif sta_flag:
        
        result = filtered[(filtered.number > 62)].iloc[0]
    
    elif promo_flag:
        
        result = filtered[filtered[relevant_keys[0]].isin([relevant_keys[1]])].iloc[-1]
            
    else:
        
        result = filtered[filtered[relevant_keys[0]].isin([relevant_keys[1]])].iloc[0]
    
    return result

def fetch_setnumber(card_info, referenceDB, verbose = False):
    '''
    Fetches the set number for a card from your binder.
    
    card_info: pd.Series A single dimentional pd.Series containing card information
    referenceDB: pd.DataFrame A dataframe containing general card information obtained via [website here]
    verbose: Bool Option to turn on debug messages.
    
    returns:
    result.number: The set number for the card in question.
    '''
    # right away we fix casing and deal with multiple treatments
    # in a single file
    treatment = card_info.treatment.lower()
    treatment = treatment.split(' (')

    
    if verbose:
        print("*"*50)
        print(card_info['name'])
        print("*"*50)
        print(f"treatment: {treatment}")
       
    # defines how we will access the information, used for
    # the diagnostics as well (see lookup function above)
    conversion_dict = {
        '' : ['borderColor', ''],
        'borderless' : ['borderColor', 'borderless'],
        'foil etched' : ['finishes', ['etched']],
        'extended art' : ['finishes', 'extended art'],
        'retro frame' : ['frameVersion', '1997'],
        'jp alternate art' : ['finishes', 'jp alt art'],
        'showcase' : ['frameEffects', ['showcase']],
        'gilded foil' : ['hasNonFoil', False],
        'dungeon module' : ['frameEffects', ['showcase']],
        # not tested yet
        'buy-a-box' : ['hasNonFoil', False]}

    # typically the first key is the defining one, will update
    # if this is no longer a rule
    relevant_keys = conversion_dict[treatment[0]]
    
    # set up processor. Depending on how complicated this gets may move logic
    # into the lookup function and have set_code become another argument
    promo_flag = len(treatment) > 1
    sta_flag = card_info.set_code == 'STA'
             
    result = lookup(name = card_info['name'],
                    relevant_keys = relevant_keys, 
                    referenceDB = referenceDB, 
                    promo_flag = promo_flag, sta_flag = sta_flag, verbose = verbose)
    
    if verbose:
        print(result.number)
        print("-"*50)
        
    return result.number