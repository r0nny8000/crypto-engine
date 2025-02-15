import pytest
import cryptoengine.kraken.marketdata as marketdata

# Generated by Copilot

def test_get_asset_data():
    """Test the `get_asset_data` function from the `marketdata` module."""

    assert marketdata.get_asset_data("BTCEUR")
    assert marketdata.get_asset_data("BTCUSD")
    assert marketdata.get_asset_data("BTC")

    assert marketdata.get_asset_data("SOLEUR")
    assert marketdata.get_asset_data("SOLUSD")
    assert marketdata.get_asset_data("SOL")

    assert marketdata.get_asset_data("ETHEUR")
    assert marketdata.get_asset_data("ETHUSD")
    assert marketdata.get_asset_data("ETH")

    assert marketdata.get_asset_data("EUR")

    assert not marketdata.get_asset_data("XXXXXX")
