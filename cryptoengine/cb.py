"""This is the cryptoengine module."""

import shutil
import click
from tabulate import tabulate
from candlestick_chart import Candle, Chart
import cryptoengine.kraken.marketdata as marketdata


@click.group()
def cli():
    """add a group of commands to the command line interface."""



@cli.command()
@click.argument('pair', required=True)
def value(pair):
    """
    Fetch and display the bid price for a given currency pair from the Kraken public API.

    Args:
        pair (str): A currency pair (e.g., 'BTCUSD').

    Returns:
        None: This function does not return a value. It prints the bid price to the console.
    """

    data = marketdata.value(pair)

    if data is None:
        click.echo(click.style("Failed to retrieve ticker information.", fg="red"))
        return

    click.echo(data)

@cli.command()
@click.argument('currencies', required=True)
def values(currencies):
    """Get the values for a given currencies in USD, EUR, BTC and ETH (if available)."""

    data = marketdata.values(currencies)

    if data is None:
        click.echo(click.style("Failed to retrieve ticker information.", fg="red"))
        return

    # Prepare data for tabulate
    table = []
    for key in data:  # pylint: disable=consider-using-dict-items
        row = [key]
        row.append(data[key].get("EUR", "-"))
        row.append(data[key].get("USD", "-"))
        row.append(data[key].get("BTC", "-"))
        row.append(data[key].get("ETH", "-"))
        table.append(row)

    # Print table using tabulate
    click.echo(
        tabulate(
            table,
            headers=["Currency", "EUR", "USD", "BTC", "ETH"],
            tablefmt="rounded_grid"
        )
    )


@cli.command()
@click.argument('pair', required=True)
@click.option('--interval', '--i', show_default=True, default="1w", help="Display a candlestick chart for the given interval: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 2w") # pylint: disable=line-too-long
@click.option('--volume', '--v', is_flag=True, flag_value=True, help="Display the volume.") # pylint: disable=line-too-long
def chart(pair, interval, volume):
    """
    Generates and displays a candlestick chart for a given trading pair and interval.

    Args:
        pair (str): The trading pair to generate the chart for (e.g., 'BTC/USD').
        interval (str): The time interval for the chart data (e.g., '1h', '1d').

    Returns:
        None
    """

    data = marketdata.get_ohlc_data(pair, interval)

    candles = []
    for d in data:
        candles.append(
            Candle(timestamp=d[0], open=d[1], high=d[2], low=d[3], close=d[4], volume=d[6])
        )

    # Optional keyword arguments: title, width, height
    c = Chart(candles, title=pair.upper())
    c.update_size(shutil.get_terminal_size().columns - 2, shutil.get_terminal_size().lines - 6)  # pylint: disable=line-too-long
    c.set_volume_pane_enabled(volume)
    c.draw()


if __name__ == "__main__":
    cli()  # Call the main function to start the command line interface.
