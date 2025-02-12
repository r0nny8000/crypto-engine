"""This is the cryptoengine module."""

import shutil
import click
from tabulate import tabulate
from candlestick_chart import Candle, Chart
import cryptoengine.kraken.marketdata as marketdata
import cryptoengine.kraken.accountdata as accountdata
from datetime import datetime


@click.group()
def cli():
    """add a group of commands to the command line interface."""



@cli.command()
@click.argument('pair', required=True)
def value(pair):
    """Fetch and display the bid price for a given currency pair from the Kraken public API."""

    data = marketdata.get_value(pair)

    if data is None:
        click.echo(click.style("Failed to retrieve ticker information.", fg="red"))
        return

    click.echo(data)


@cli.command()
@click.argument('pair', required=True)
@click.option('--interval', '--i', show_default=True, default="1w",
              help="Display a candlestick chart for: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 2w")
@click.option('--volume', '--v', is_flag=True, flag_value=True, help="Display the volume.") # pylint: disable=line-too-long
@click.option('--heikin_ashi', '--ha', is_flag=True, flag_value=True, help="Display the Heikin-Ashi chart.") # pylint: disable=line-too-long
def chart(pair, interval, volume, heikin_ashi):
    """Generates and displays a candlestick chart for a given trading pair and interval."""

    data = marketdata.get_ohlc_data(pair, interval)

    candles = []
    previous = {}
    for d in data:

        d = [float(i) for i in d] # Convert all values to floats

        if (heikin_ashi):
            if not previous:
                previous = d
            else:
                d[1] = (previous[1] + previous[4]) / 2
                d[2] = max(d[2], d[1])
                d[3] = min(d[3], d[1])
                d[4] = (d[1] + d[2] + d[3] + d[4]) / 4
                previous = d

        candles.append(
            Candle(timestamp=d[0], open=d[1], high=d[2], low=d[3], close=d[4], volume=d[6])
        )

    # Optional keyword arguments: title, width, height
    c = Chart(candles, title=pair.upper())
    c.update_size(shutil.get_terminal_size().columns - 2, shutil.get_terminal_size().lines - 6)  # pylint: disable=line-too-long
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
            continue # Skip zero balances
        row.append(quantity)

        # third column is the balance in EUR
        current_value = marketdata.get_value(asset + "EUR")
        if not current_value:
            current_value = marketdata.get_value(asset + "ZEUR")
        if current_value:
            row.append(round(quantity * current_value, 2))

        # finally, add the row to the table
        table.append(row)

    click.echo(
        tabulate(
            table,
            headers=["Currency", "Balance", "EUR"],
            tablefmt="rounded_grid"
        )
    )



def convert_time(timestamp):
    """Convert a Unix timestamp to a human-readable date and time string."""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


@cli.command()
@click.option('--all_orders', '--a', is_flag=True, flag_value=True, help="Include all orders.") # pylint: disable=line-too-long
def orders(all_orders):
    """Retrieves and displays a table of open and optionally closed orders."""
    
    open_orders = accountdata.get_open_orders()
    closed_orders = accountdata.get_closed_orders()

    latest_orders = {}
    latest_orders.update(open_orders["open"])
    if all_orders:
        latest_orders.update(closed_orders["closed"])
    else:
        for closed_order_key, closed_order in closed_orders["closed"].items():
            if datetime.now().timestamp() - closed_order["closetm"] < 2592000:  # 2592000 seconds = 30 days
                latest_orders.update({closed_order_key: closed_order})

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
            convert_time(order["opentm"])
        ]

        if "closetm" in order.keys():
            row.append(convert_time(order["closetm"]))

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


if __name__ == "__main__":
    cli()  # Call the main function to start the command line interface.
