"""This is the cryp2bot module."""

import click
from tabulate import tabulate
import cryp2bot.kraken.marketdata as marketdata


@click.group()
def cli():
    """add a group of commands to the command line interface."""


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


if __name__ == "__main__":
    cli()  # Call the main function to start the command line interface.
