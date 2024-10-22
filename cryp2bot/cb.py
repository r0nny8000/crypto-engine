"""This is the cryp2bot module."""

import click
import cryp2bot.kraken.marketdata as marketdata


@click.group()
def cli():
    """add a group of commands to the command line interface."""
    pass # This is a no-op

@cli.command()
@click.argument('command', required=True)
@click.argument('parameter')
def kraken(command, parameter):
    """Translates commands to API calls for the Kraken exchange."""
    if command == "ticker":
        marketdata.ticker(parameter)
    else:
        click.echo(click.style("UNKNOWN COMMAND", fg="red"))


if __name__ == "__main__":
    #click.echo(click.style("Hello, I am the cryp2 bot.", fg="green"))
    cli() # Call the main function
