fut
=====

.. image:: https://travis-ci.org/oczkers/fut.png?branch=master
        :target: https://travis-ci.org/oczkers/fut

fut is a simple library for managing Fifa Ultimate Team.
It is written entirely in Python.



Documentation
-------------
Documentation is available at http://fut.readthedocs.org/.

Players database: http://cdn.content.easports.com/fifa/fltOnlineAssets/8D941B48-51BB-4B87-960A-06A61A62EBC0/2015/fut/items/web/players.json



Usage
-----

.. code-block:: pycon

    >>> import fut
    >>> fut = fut.Core('email', 'password', 'secret answer', platform='xbox', emulate='and', debug=True, cookies='cookies.txt')
    >>> # PLATFORM: pc / ps3 / xbox / and / ios     (pc default)
    >>> # EMULATE: and / ios (use this feature to avoid webapp errors [BE WARE IT'S HIGH RISK])
    >>> # DEBUG: save http response to fut.log)
    >>> # COOKIES: save cookies after every request and load it from given file when restaring app (just like browser)

    >>> items = fut.searchAuctions('development',  # search items
    ...     level='gold', category='fitness', min_price=300,  # optional parametrs
    ...     max_price=600, min_buy=300, max_buy=400,  # optional parametrs
    ...     start=0, page_size=50)  # optional parametrs

    >>> for item in items:
    ...     trade_id = item['tradeId']
    ...     buy_now_price = item['buyNowPrice']
    ...     trade_state = item['tradeState']
    ...     bid_state = item['bidState']
    ...     starting_bid = i['startingBid']
    ...     item_id = i['id']
    ...     timestamp = i['timestamp']  # auction start
    ...     rating = i['rating']
    ...     asset_id = i['assetId']
    ...     resource_id = i['resourceId']
    ...     item_state = i['itemState']
    ...     rareflag = i['rareflag']
    ...     formation = i['formation']
    ...     injury_type = i['injuryType']
    ...     suspension = i['suspension']
    ...     contract = i['contract']
    ...     playStyle = i['playStyle']  # used only for players
    ...     discardValue = i['discardValue']
    ...     itemType = i['itemType']
    ...     owners = i['owners']
    ...     offers = i['offers']
    ...     current_bid = i['currentBid']
    ...     expires = i['expires']  # seconds left

    >>> fut.credits  # returns credits amount
    600

    >>> fut.bid(items[0]['trade_id'], 600)  # make a bid

    >>> fut.credits  # it's updated automatically on every request
    0
    >>> fut.tradepile_size  # tradepile size (slots)
    80
    >> len(fut.tradepile())  # tradepile fulfilment (number of cards in tradepile)
    20
    >>> fut.watchlist_size  # watchlist size (slots)
    30
    >> len(fut.watchlist())  # watchlist fulfilment (number of cards in watchlist)
    10

    >>> items = fut.tradepile()  # get all items from trade pile
    >>> items = fut.unassigned()  # get all unassigned items

    >>> for item in items:
    ...     fut.sell(item['item_id'], 150,  # put item on auction
    ...              buy_now=0, duration=3600)  # optional parametrs

    >>> fut.sendToTradepile(trade_id, item_id)               # add card to tradepile
    >>> fut.sendToClub(trade_id, item_id)                    # add card to club
    >>> fut.sendToWatchlist(trade_id)                        # add card to watchlist
    >>> fut.tradepileDelete(trade_id)                        # removes item from tradepile
    >>> fut.watchlistDelete(trade_id)                        # removes item from watch list
    >>> fut.quickSell(item_id)                               # quicksell item
    >>> fut.searchDefinition(asset_id, start=0, count=35)    # returns stats and definition IDs for each card variation

    >>> fut.relist()  # relist all expired cards in tradepile

    >>> fut.keepalive()  # send keepalive ping to avoid timeout (send at least one request every ~10 minutes)

    to be continued ;-)
    ...


CLI examples
------------
.. code-block:: bash

    not yet
    ...


License
-------

GNU GPLv3
