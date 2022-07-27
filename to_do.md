Things to still do:

Main work:

[X] Connect echoMTG to price data and set number


[X] SQL Schema.
    - What questions am I trying to answer?
        - How much has a card cost, historically? (needs to be a table that has card_ids and price in... long format?)

[ ] Fix Nones being stuffed where Falses should go due to function logic
[ ] Fix Mana Cost for ZNR double-faced cards that have land drops.
[ ] Fix Legalities -> use ints to represent. Legality will be a 12-bit number.
[ ] Build account creation
[ ] Add CSV upload
[ ] Add echoMTG api connection
[ ] Add scryfall api connection for pricing
[ ] Over / Under $1 indicator


Low Priority:

[ ] Get Legalities Working
[ ] Get colors + colorIdentity working
[ ] Consider if there is a better way for storage of current data types
[ ] Have Log-In accept email and account name
[ ] *Upgrade code to SQLAlchemy w/ SQLite hooks in backend*

All of these things are dependant on the above:
- Add option to pull new values / new inventory
- Add option to just pull price based on the cards I am looking at in my inventory.
- Set aside cards under and over \$1.


At the end:
- Run through and properly comment / document