"""This is the cryp2bot module."""

import click
import cryp2bot.kraken.marketdata as marketdata
from tabulate import tabulate


@click.group()
def cli():
    """add a group of commands to the command line interface."""


@cli.command()
@click.argument('currency', required=True)
def value(currency):
    """Get the ticker information for a given currency."""
    
    currency = currency.upper()

    if currency is None or currency.strip() == "":
        click.echo(click.style("The argument is required.", fg="red"))
        return

    data = marketdata.value(currency)

    if data is None:
        click.echo(click.style("Failed to retrieve ticker information.", fg="red"))
        return

    # Prepare data for tabulate
    table = []
    for key in data:
        row = [key]
        row.append(data[key].get("EUR", "-"))
        row.append(data[key].get("USD", "-"))
        row.append(data[key].get("BTC", "-"))
        row.append(data[key].get("ETH", "-"))
        table.append(row)

    # Print table using tabulate
    click.echo(tabulate(table, headers=["Currency", "EUR", "USD", "BTC", "ETH"]))

if __name__ == "__main__":
    cli()  # Call the main function to start the command line interface.
