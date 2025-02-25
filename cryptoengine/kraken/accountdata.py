"""
This module provides functionality to interact with the Kraken API 
to fetch account balance information.
"""

from datetime import datetime
import os
import logging
from kraken.spot import User, Trade
from cryptoengine.kraken import marketdata

LOGGING_FORMAT = "%(asctime)s %(levelname)-8s %(funcName)-16s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT, filename="/tmp/crypto-engine.log")

user = User(key=os.getenv('KRAKEN_API_KEY'), secret=os.getenv('KRAKEN_API_SECRET')) 
trade = Trade(key=os.getenv('KRAKEN_API_KEY'), secret=os.getenv('KRAKEN_API_SECRET'))

def get_balance():
    """Fetches and returns the account balance from Kraken."""
    return user.get_account_balance()

def get_orders(all_orders=False):
    """Fetches and prints the orders from Kraken."""

    open_orders = get_open_orders()
    closed_orders = get_closed_orders()

    latest_orders = {}
    latest_orders.update(open_orders["open"])
    if all_orders:
        latest_orders.update(closed_orders["closed"])
    else:
        for closed_order_key, closed_order in closed_orders["closed"].items():
            if datetime.now().timestamp() - closed_order["closetm"] < 2592000:
                # 2592000 s = 30 days
                latest_orders.update({closed_order_key: closed_order})
    
    return latest_orders


def get_closed_orders():
    """Fetches and prints the closed orders from Kraken."""
    return user.get_closed_orders()

def get_open_orders():
    """Fetches and prints the open orders from Kraken."""
    return user.get_open_orders()


def buy(asset, volume, currency):
    """Creates a buy order on Kraken."""


    # Check if the asset exists
    asset = marketdata.get_asset_data(asset + currency)

    if not asset:
        logging.error('Invalid asset pair %s.', asset)
        return None

    # Chech if the volume is a valid number
    try:
        volume = float(volume)

    except ValueError:
        logging.error('Invalid volume %s.', volume)
        return None
    
    if volume < 1:
        logging.error('The volume of %s is too small. Volume needs to be higher than 1.', volume)
        return None

    # Check if the user has enough balance
    balance = get_balance()

    pair = None
    for k in asset.keys():
        pair = k
        break

    quote = None
    for a in asset.values():
        quote = a["quote"]
        break

    # Check if the quote currency exists in the balance
    if quote not in balance.keys():
        logging.error('No balance for the selected currency %s ', currency)
        return None

    # Check if the user has enough balance
    if float(balance[quote]) < volume:
        logging.error('Insufficient balance of %s.', currency)
        return None

    # Get the current value for the limit order
    limit_price = round(marketdata.get_value(pair) * 1.001, 2)

    if not limit_price:
        logging.error('Did not get limit price for the selected currency %s ', currency)
        return None

    # translate currency to assest => volume
    asset_volume = round(volume / marketdata.get_value(pair), 4)

    if asset_volume < 0.002:
        logging.error('The asset volume of %s is too small. Volume needs to be higher than 0.002.', asset_volume)
        return None


    # Create a limit order
    return create_order(pair, 'buy', asset_volume, 'limit', round(limit_price / 10, 2))



def create_order(pair, side, volume, ordertype, limit_price):
    """Creates an order on Kraken."""
    try:
        transaction = trade.create_order(pair=pair,
                                        side=side,
                                        volume=volume,
                                        ordertype=ordertype,
                                        price=limit_price)
    except Exception as e:
        logging.error('%s %s', pair, str(e).replace('\n', ' '))
        print(e)
        return None

    return transaction
