"""
This module provides functionality to fetch and display the bid prices
for given currency pairs from the Kraken public API.
"""

import logging
import json
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')

def value(currencies):
    """
    Fetches and returns the bid prices for the given currency pairs from the Kraken public API.

    Args:
        pairs (str): A comma-separated string of currency pairs.

    Returns:
        dict: A dictionary with currency pairs as keys and their bid prices as values.
    """

    pairs = ""

    for c in currencies.split(','):
        if len(pairs) > 0:
            pairs += ","
        pairs += c + "EUR" + "," + c + "USD"
        if c.upper() != "BTC":
            pairs += "," + c + "BTC"
        if c.upper() != "ETH" and c.upper() != "BTC":
            pairs += "," + c + "ETH"

    pairs = pairs.upper()

    valid_pairs = ""
    for p in pairs.split(','):
        if get_asset_data(p) is None:
            logging.error("%s is not a valid currency pair.", p)
        else:
            if len(valid_pairs) > 0:
                valid_pairs += ","
            valid_pairs += p

    logging.debug("Valid pairs: %s ", {valid_pairs})

    url_ticker = "https://api.kraken.com/0/public/Ticker?pair=" + valid_pairs
    headers = {
        'Accept': 'application/json'
    }

    try:
        response_ticker = requests.get(url_ticker, headers=headers, timeout=4).json()
        if len(response_ticker['error']) > 0:
            logging.error("Error: %s", json.dumps(response_ticker['error'], indent=4))
        if 'result' not in response_ticker:
            logging.error("No result in response of ticker request.")
    except requests.RequestException as e:
        logging.error('Request failed: %s', e)
        return {}

    values = {}
    for key in response_ticker.get('result', {}):
        asset_name = get_asset_name(key)
        asset_value_name = get_asset_value_name(key)
        asset_value = float(response_ticker['result'][key]['b'][0])

        if asset_name not in values:
            values[asset_name] = {}

        if (asset_value_name == 'EUR' or asset_value_name == 'USD'):
            asset_value = round(asset_value, 2)
        else:
            asset_value = round(asset_value, 8)

        values[asset_name][asset_value_name] = asset_value

    return values

def get_asset_name(key):
    """
    Extracts the asset name from the given assets dictionary.

    Args:
        key (str): The key to look up in the assets dictionary.

    Returns:
        str: The name of the asset before the '/' character in the 'wsname' field.
    """
    asset = get_asset_data(key)
    if asset is None:
        return key
    return asset['result'][key]['wsname'][:asset['result'][key]['wsname'].find('/')].replace('XBT', 'BTC') # pylint: disable=line-too-long

def get_asset_value_name(key):
    """
    Extracts the asset value name from the given assets dictionary.

    Args:
        key (str): The key to look up in the assets dictionary.

    Returns:
        str: The name of the asset after the '/' character in the 'wsname' field, 
        with 'XBT' replaced by 'BTC'.
    """
    asset = get_asset_data(key)
    if asset is None:
        return key
    value_name = asset['result'][key]['wsname']
    return value_name[value_name.find('/')+1:].replace('XBT', 'BTC')

def get_asset_data(pair):
    """
    Fetches asset data for a given trading pair from the Kraken API.

    Args:
        pair (str): The trading pair for which to fetch asset data (e.g., 'XXBTZUSD').

    Returns:
        dict or None: A dictionary containing the asset data if the request is 
        successful and the 'result' key is present in the response.
        Returns None if the request fails or the 'result' key is not present in the response.
    Raises:
        requests.RequestException: If there is an issue with the HTTP request.
    """
    url_asset = "https://api.kraken.com/0/public/AssetPairs?pair=" + pair
    headers = {
        'Accept': 'application/json'
    }

    try:
        response_asset = requests.get(url_asset, headers=headers, timeout=4).json()
    except requests.RequestException as e:
        logging.error("Request failed: %e", e)
        return None

    return response_asset if 'result' in response_asset else None
