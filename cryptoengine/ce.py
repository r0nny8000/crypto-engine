"""This is the cryptoengine module."""

from datetime import datetime
import shutil
import click
from tabulate import tabulate
from candlestick_chart import Candle, Chart
from cryptoengine.kraken import marketdata
from cryptoengine.kraken import accountdata


@click.group()
def cli():
    """add a group of commands to the command line interface."""


@cli.command()
@click.argument('pair', required=True)
def value(pair):
    """Fetch and display the bid price for a given currency pair from the Kraken public API."""

    data = marketdata.get_value(pair)

    if data is None:
        click.echo(click.style(
            "Failed to retrieve ticker information.", fg="red"))
        return

    click.echo(data)


@cli.command()
@click.argument('pair', required=True)
@click.option('--interval', '--i', show_default=True, default="1d",
              help="Display a candlestick chart for: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 2w")
@click.option('--volume', '--v', is_flag=True, flag_value=True, help="Display the volume.")  # pylint: disable=line-too-long
@click.option('--heikin_ashi', '--ha', is_flag=True, flag_value=True, help="Display the Heikin-Ashi chart.")  # pylint: disable=line-too-long
def chart(pair, interval, volume, heikin_ashi):
    """Generates and displays a candlestick chart for a given trading pair and interval."""

    data = marketdata.get_ohlc_data(pair, interval)

    if not data:
        click.echo(click.style(
            "Failed to retrieve OHLC data. Maybe the asset or pair is unknown.", fg="red"))
        return

    candles = []
    previous = {}
    for d in data:

        d = [float(i) for i in d]  # Convert all values to floats

        if heikin_ashi:
            if not previous:
                previous = d
            else:
                d[1] = (previous[1] + previous[4]) / 2
                d[2] = max(d[2], d[1])
                d[3] = min(d[3], d[1])
                d[4] = (d[1] + d[2] + d[3] + d[4]) / 4
                previous = d

        candles.append(
            Candle(timestamp=d[0], open=d[1], high=d[2],
                   low=d[3], close=d[4], volume=d[6])
        )

    # Optional keyword arguments: title, width, height
    c = Chart(candles, title=pair.upper())
    c.update_size(shutil.get_terminal_size().columns - 2,
                  shutil.get_terminal_size().lines - 6)  # pylint: disable=line-too-long
    c.set_volume_pane_enabled(volume)
    c.draw()


@cli.command()
def balance():
    """Get the balance of the account."""
    b = accountdata.get_balance()

    table = []
    for asset in b:

        # first column is the currency name
        row = [marketdata.get_asset_name(asset)]

        # second column is the balance
        quantity = float(b[asset])
        if not quantity:
            continue  # Skip zero balances
        row.append(quantity)

        # third column is the balance in EUR
        current_value = marketdata.get_value(asset)
        if current_value and asset != "ZEUR":
            row.append(round(quantity * current_value, 2))

        # finally, add the row to the table:
        table.append(row)

    click.echo(
        tabulate(
            table,
            headers=["Currency", "Balance", "EUR"],
            tablefmt="rounded_grid"
        )
    )


@cli.command()
@click.option('--all_orders', '--a', is_flag=True, flag_value=True, help="Include all orders.")  # pylint: disable=line-too-long
def orders(all_orders):
    """Retrieves and displays a table of open and optionally closed orders."""

    latest_orders = accountdata.get_orders(all_orders)

    table = []
    for order_key, order in latest_orders.items():
        order = latest_orders[order_key]

        row = [
            order_key,
            order["status"],
            order["descr"]["pair"],
            order["descr"]["type"],
            order["descr"]["ordertype"],
            order["descr"]["price"],
            order["vol"],
            order["cost"],
            order["fee"],
            datetime.fromtimestamp(order["opentm"]).strftime(
                '%Y-%m-%d %H:%M:%S')
        ]

        if "closetm" in order.keys():
            row.append(datetime.fromtimestamp(
                order["opentm"]).strftime('%Y-%m-%d %H:%M:%S'))

        table.append(row)

    table.reverse()

    click.echo(
        tabulate(
            table,
            headers=[
                "Order ID", "Status", "Pair", "Type", "Order Type",
                "Price", "Volume", "Cost", "Fee", "Open Time", "Close Time"
            ],
            missingval="-",
            tablefmt="rounded_grid"
        )
    )


@cli.command()
@click.argument('asset', required=True, type=click.STRING)
@click.argument('volume', required=True, type=click.FLOAT)
@click.argument('currency', required=False, type=click.STRING, default="EUR")
def buy(asset, volume, currency):
    """Buy an asset with a given volume and currency.

    \b
    ASSET to buy, eg. ETH, BTC, XRP. (left part of the pair)
    VOLUME of the asset to buy with the exchange currency, eg EUR or USD(T).
    CURRENCY to use for the purchase. Default is EUR. (right part of the pair)

    """

    click.echo('Buying %s with %s %s...' % (asset, volume, currency))

    transaction = accountdata.buy(asset, volume, currency)

    if transaction:
        click.echo(click.style("Created order successfully: " +
                   str(transaction['descr']['order']) + ".", fg="green"))
    else:
        click.echo(click.style("Failed to create order.", fg="red"))


@cli.command()
@click.argument('asset', required=True)
@click.argument('volume', required=True)
def dca(asset, volume):
    """Dollar cost average into an asset with a given volume."""

    click.echo('Dollar cost averaging into %s with %s EUR...', asset, volume)

    transaction = accountdata.dca(asset, volume)

    if transaction:
        click.echo(click.style("Created order successfully: " +
                   str(transaction['descr']['order']) + ".", fg="green"))
    else:
        click.echo(click.style("Failed to create order.", fg="red"))


if __name__ == "__main__":
    cli()  # Call the main function to start the command line interface..
