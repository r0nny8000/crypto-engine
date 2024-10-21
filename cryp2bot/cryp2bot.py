"""This is the cryp2bot module."""

import click
from cryp2bot.kraken import marketdata


@click.group()
def cli():
    """add a group of commands to the command line interface."""
    pass # This is a no-op

@cli.command()
# @click.option('--count', default=1, help='number of greetings')
@click.argument('command')
def kraken(command):
    """Function that greets a person."""
    if command == "server_time":
        marketdata.server_time()
    else:
        click.echo(click.style("Unknown command", fg="red"))


if __name__ == "__main__":
    click.echo(click.style("Hello, I am the cryp2 bot", fg="green"))
    cli() # Call the main function
