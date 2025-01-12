"""
This module provides functionality to fetch and display the bid prices
for given currency pairs from the Kraken public API.
"""

import logging

from kraken.spot import Market
from kraken.exceptions import * # pylint: disable=wildcard-import,unused-wildcard-import


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

def get_ohlc_data(pair, interval):
    """
    Fetches OHLC (Open, High, Low, Close) data for a given currency pair 
    and interval from the Kraken API.

    Args:
        pair (str): The currency pair to fetch data for (e.g., 'XXBTZUSD').
        interval (str): The interval for the OHLC data. Valid intervals are:
                        '1m' (1 minute), '5m' (5 minutes), '15m' (15 minutes),
                        '30m' (30 minutes), '1h' (1 hour), '4h' (4 hours),
                        '1d' (1 day), '1w' (1 week), '2w' (2 weeks).
    Returns:
        dict: An array containing the OHLC data if the request is successful.
              [int <time>, string <open>, string <high>, string <low>, string <close>, 
              string <vwap>, string <volume>, int <count>]
              Returns None if the currency pair is invalid or if the request fails.
              
    Raises:
        requests.RequestException: If there is an issue with the HTTP request.
    """

    if get_asset_data(pair) is None:
        logging.error("%s is not a valid currency pair.", pair)
        return None

    intervals = {}
    intervals['1m'] = 1
    intervals['5m'] = 5
    intervals['15m'] = 15
    intervals['30m'] = 30
    intervals['1h'] = 60
    intervals['4h'] = 240
    intervals['1d'] = 1440
    intervals['1w'] = 10080
    intervals['2w'] = 21600

    try:
        ohlc =  Market().get_ohlc(pair, intervals[interval])

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError, KrakenInvalidArgumentsError) as e:
        logging.error('An unexpected error with %s occurred: %s', pair, str(e).replace('\n', ' '))
        return None

    data = []
    for v in ohlc.values():
        data = v
        break

    return data


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
    try:
        data =  Market().get_asset_pairs(pair)

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError) as e:
        logging.error('An unexpected error with %s occurred: %s', pair, str(e).replace('\n', ' '))
        return None

    return data

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

    logging.info("Fetching ticker data for %s...", pair)

    try:
        data = Market().get_ticker(pair)

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError) as e:
        logging.error('An unexpected error occurred: %s', e)
        return None

    logging.info("Ticker data fetched successfully.")
    return data
