"""
This module provides functionality to fetch and display the bid prices
for given currency pairs from the Kraken public API.
"""

import json
import requests

def price(pairs):
    """
    Fetches and returns the bid prices for the given currency pairs from the Kraken public API.

    Args:
        pairs (str): A comma-separated string of currency pairs.

    Returns:
        dict: A dictionary with currency pairs as keys and their bid prices as values.
    """
    
    url_ticker = "https://api.kraken.com/0/public/Ticker?pair=" + pairs
    url_asset = "https://api.kraken.com/0/public/AssetPairs?pair=" + pairs


    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    ticker = requests.request("GET", url_ticker, headers=headers, data=payload, timeout=4).json()
    assets = requests.request("GET", url_asset, headers=headers, data=payload, timeout=4).json()

    if 'result' not in ticker:
        return None
    
    if 'result' not in assets:
        return None
    
    #print(json.dumps(response, indent=4))
    
    keys = list(ticker['result'].keys())

    prices = {}

    for key in keys:
        asset = assets['result'][key]['wsname'].replace('XBT', 'BTC')
        prices[asset] = float(ticker['result'][key]['b'][0])
        
    
    return prices
