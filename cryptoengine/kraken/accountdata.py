"""
This module provides functionality to interact with the Kraken API 
to fetch account balance information.
"""

from datetime import datetime
import os
from kraken.spot import User


user = User(key=os.getenv('KRAKEN_API_KEY'), secret=os.getenv('KRAKEN_API_SECRET')) # authenticated

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