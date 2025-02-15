"""
This module provides functionality to fetch and display the bid prices
for given currency pairs from the Kraken public API.
"""

import logging

from kraken.spot import Market
from kraken.exceptions import * # pylint: disable=wildcard-import,unused-wildcard-import


LOGGING_FORMAT = "%(asctime)s %(levelname)-8s %(funcName)-16s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT, filename="/tmp/crypto-engine.log")


def get_asset_name(pair):
    """Fetches the asset name for a given trading pair from the Kraken API."""

    asset = get_asset_data(pair)

    if not asset:
        return None
    else:
        for a in asset.values():
            wsname = a['wsname']
            name = wsname[:wsname.find('/')]
            return name.replace('XBT', 'BTC')

        return None


def get_asset_data(pair):
    """Fetches asset data for a given trading pair from the Kraken API."""

    asset_pairs = None

    if len(pair) <= 4:
        asset_pairs = get_asset_pairs(pair + 'ZEUR')

        if not asset_pairs:
            asset_pairs = get_asset_pairs(pair + 'EUR')

        if not asset_pairs:
            asset_pairs = get_asset_pairs(pair + 'ZUSD')
        
        if not asset_pairs:
            asset_pairs = get_asset_pairs(pair + 'USD')

    else:
        asset_pairs = get_asset_pairs(pair)

    return  asset_pairs

def get_asset_pairs(pair):

    try:

        asset_pairs = Market().get_asset_pairs(pair)

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError) as e:
        logging.error('%s %s', pair, str(e).replace('\n', ' '))
        return None

    return  asset_pairs if asset_pairs else None



def get_value(pair):
    """Fetches and returns the bid price for a given currency pair from the Kraken public API."""

    result = None


    if len(pair) <= 4:
        result = get_ticker(pair + 'ZEUR')

        if not result:
            result = get_ticker(pair + 'EUR')

        if not result:
            result = get_ticker(pair + 'ZUSD')
        
        if not result:
            result = get_ticker(pair + 'USD')


    else:
        result = get_ticker(pair)

    if not result:
        return None

    asset_value = 0.0
    for v in result.values():
        asset_value = float(v['b'][0])
    return round(asset_value, 2)


def get_ticker(pair):
    """Fetches ticker data for a given trading pair from the Kraken API."""

    logging.info("Fetching ticker data for %s...", pair)

    try:

        ticker = Market().get_ticker(pair)

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError) as e:
        logging.error('%s: %s', pair, str(e).replace('\n', ' '))
        return None

    logging.info("Ticker data fetched successfully.")
    return ticker


def get_ohlc_data(pair, interval):
    """Fetches OHLC (Open, High, Low, Close) data for a given currency pair 
    and interval from the Kraken API."""

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
        logging.error('%s: %s', pair, str(e).replace('\n', ' '))
        return None


    data = []
    for v in ohlc.values():
        data = v
        break

    return data
