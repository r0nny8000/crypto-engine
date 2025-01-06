"""
This module provides functionality to fetch and display the bid prices
for given currency pairs from the Kraken public API.
"""

import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')


def value(pair):
    """
    Fetches and returns the bid price for a given currency pair from the Kraken public API.

    Args:
        pair (str): A currency pair.

    Returns:
        float or None: The bid price for the currency pair, rounded to 2 decimal places, 
        or None if the pair is invalid or the ticker information could not be retrieved.
    """
    if get_asset_data(pair) is None:
        logging.error("%s is not a valid currency pair.", pair)
        return None

    result = get_ticker(pair)

    if result is None:
        logging.error("Failed to retrieve ticker information.")
        return None

    asset_value = 0.0
    for v in result.values():
        asset_value = float(v['b'][0])
    return round(asset_value, 2)

def values(currencies):
    """
    Fetches and returns the bid prices for the given currency pairs from the Kraken public API.

    Args:
        currencies (str): A comma-separated string of currency pairs.

    Returns:
        dict: A dictionary with currency pairs as keys and their bid prices as values.
    """
    pairs = ""

    for c in currencies.upper().split(','):
        for a in ["EUR", "USD", "BTC", "ETH"]:
            p = c + a
            if get_asset_data(p) is None:
                logging.error("%s is not a valid currency pair.", p)
            else:
                if len(pairs) > 0:
                    pairs += ","
                pairs += p

    response = get_ticker(pairs)

    if response is None:
        return None

    asset_values = {}

    for pair in response:
        asset_name_left = get_asset_name_left(pair)
        asset_name_right = get_asset_name_right(pair)
        asset_value = float(response[pair]['b'][0])

        if asset_name_left not in asset_values:
            asset_values[asset_name_left] = {}

        if asset_name_right in ['EUR', 'USD']:
            asset_value = round(asset_value, 2)
        else:
            asset_value = round(asset_value, 8)

        asset_values[asset_name_left][asset_name_right] = asset_value

    return asset_values

def get_asset_name_left(pair):
    """
    Extracts the left part of the asset name from the given assets pair.

    Args:
        key (str): The key to look up in the assets dictionary.

    Returns:
        str: The name of the asset before the '/' character in the 'wsname' field.
    """
    asset = get_asset_data(pair)
    if asset is None:
        return pair
    return asset[pair]['wsname'][:asset[pair]['wsname'].find('/')].replace('XBT', 'BTC')


def get_asset_name_right(pair):
    """
    Extracts the asset value name from the given assets dictionary.

    Args:
        key (str): The key to look up in the assets dictionary.

    Returns:
        str: The name of the asset after the '/' character in the 'wsname' field, 
        with 'XBT' replaced by 'BTC'.
    """
    asset = get_asset_data(pair)
    if asset is None:
        return pair
    return asset[pair]['wsname'][asset[pair]['wsname'].find('/')+1:].replace('XBT', 'BTC')


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
        response = requests.get(url_asset, headers=headers, timeout=4).json()
    except requests.RequestException as e:
        logging.error("Request failed: %e", e)
        return None

    return response['result'] if 'result' in response else None

def get_ticker(pair):
    """
    Fetches ticker data for a given trading pair from the Kraken API.

    Args:
        pair (str): The trading pair for which to fetch ticker data (e.g., 'XXBTZUSD').

    Returns:
        dict or None: A dictionary containing the ticker data if the request is 
        successful and the 'result' key is present in the response.
        Returns None if the request fails or the 'result' key is not present in the response.
    Raises:
        requests.RequestException: If there is an issue with the HTTP request.
    """

    logging.info(pair)
    url = "https://api.kraken.com/0/public/Ticker?pair=" + pair
    headers = {'Accept': 'application/json'}

    try:
        response = requests.get(url, headers=headers, timeout=4).json()

        if len(response['error']) > 0:
            logging.error("Error: %s", response['error'])

        if 'result' not in response:
            logging.error("No result in response of ticker request.")

    except requests.RequestException as e:
        logging.error('Request failed: %s', e)
        return None

    else:
        return response['result'] if 'result' in response else None
