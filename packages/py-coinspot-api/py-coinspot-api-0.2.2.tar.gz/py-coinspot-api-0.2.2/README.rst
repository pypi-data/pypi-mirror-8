Python Coinspot API Library
===========================

|Build Status|

A python library for the Coinspot API.

Copyright (C) 2014 Peter Dyson pete@geekpete.com

Source: http://github.com/geekpete/py-coinspot-api

PyPi: https://pypi.python.org/pypi/py-coinspot-api/

Please see https://www.coinspot.com.au/api for documentation on the
CoinSpot API.

**NOTE:** All requests and responses will be JSON

Installation
============

::

    pip install py-coinspot-api --user

or

::

    sudo pip install py-coinspot-api

Configuration
=============

You have two options for configuration, using os environment variables
or a yaml file

Option 1
========

Windows:

::

    set COINSPOT_API_KEY=XXXXXX
    set COINSPOT_API_SECRET=XXXXXXXXXX

Linux:

::

    export COINSPOT_API_KEY=XXXXXX
    export COINSPOT_API_SECRET=XXXXXXXXXX

Option 2
========

The config.yml.sample needs to be copied to config.yml and your unique
api key and secret values need to be inserted. Extra options like debug
and logging file name can only be configured using the yaml file.

::

    api:
     key: 'PUT_YOUR_KEY_HERE'
     secret: 'PUT_YOUR_SECRET_HERE'
     endpoint: 'www.coinspot.com.au'
    debug: True
    logfile: 'coinspot.log'

Class Documentation
===================

http://py-coinspot-api.readthedocs.org/en/latest/

TODO
====

-  Extend test cases and requirements.

Example Usage
=============

After you have your config.yml in place, test it out


::

    from coinspot import CoinSpot

    # initialise the library
    client = CoinSpot()

    # get the spot prices
    print client.spot()

    # get your coin wallet balances
    print client.balances()

    # get the last 1000 orders for Dogecoins
    print client.orderhistory('DOGE')

    # get a list of all the current buy and sell orders
    print client.orders('DOGE')

    # put an order in to sell 20 Dogecoins at 0.000280 per coin
    print client.sell('DOGE', '20', '0.000280')

    # Get a quote on buying a billion Dogecoins, with estimation of timeframe
    print client.quotebuy('DOGE', 1000000000)

    # Donate a craptonne of Dogecoins
    # to the author of this library! Much Appreciate!!!
    print client.send('DOGE', 'DJrHRxurwQoBUe7r9RsMkMrTxj92wXd5gs', 1000)

Send Dogecoins of appreciation
==============================

If you like this software, you can always send cold hard cryptocoin my
way

::

    Dogecoin: DJrHRxurwQoBUe7r9RsMkMrTxj92wXd5gs
    Bitcoin: 1LybpYphZJqSAxjNFqjfYHB8pWxKcBmFkf

You can do this using the library like this:
::

    # Donate a craptonne of Dogecoins to the author of this library!
    # Much Appreciate!!!
    print client.send('DOGE', 'DJrHRxurwQoBUe7r9RsMkMrTxj92wXd5gs', 10000)

or send Bitcoins:
::

    # Donate a craptonne of Bitcoins to the author of this library!
    print client.send('BTC', '1LybpYphZJqSAxjNFqjfYHB8pWxKcBmFkf', 1)

License
=======

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

Change Log
==========

-  0.1.1 Initial Release
-  0.2.0 Logging Support, Initial Test Cases, Exception Handling, Travis
   Support, Configuration File

.. |Build Status| image:: https://api.travis-ci.org/geekpete/py-coinspot-api.png?branch=master
   :target: https://travis-ci.org/geekpete/py-coinspot-api
