Things to still do:

Main work:

[X] Connect echoMTG to price data and set number


[X] SQL Schema.
    - What questions am I trying to answer?
        - How much has a card cost, historically? (needs to be a table that has card_ids and price in... long format?)


[ ] Fix Legalities -> need to create separate table that holds the legality information
[ ] Build account creation
[ ] Add CSV upload
[ ] Add echoMTG api connection
[ ] Add scryfall api connection for pricing
[ ] Over / Under $1 indicator




All of these things are dependant on the above:
- Add option to pull new values / new inventory
- Add option to just pull price based on the cards I am looking at in my inventory.
- Set aside cards under and over \$1.


At the end:
- Run through and properly comment / document