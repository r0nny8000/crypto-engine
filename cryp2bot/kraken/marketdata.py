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
    
    url = "https://api.kraken.com/0/public/Ticker?pair=" + pairs

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=4).json()
    
    if 'result' not in response:
        return None
    
    #print(json.dumps(response, indent=4))
    
    keys = list(response['result'].keys())

    prices = {}

    for key in keys:
        prices[key] = float(response['result'][key]['b'][0])
        
    
    return prices
