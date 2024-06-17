"""This is the cryp2bot module."""

import click
from cryp2bot.bitget.bitget import usebitget


@click.group()
def cli():
    """add a group of commands to the command line interface."""
    pass

@cli.command()
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
def hello(count, name):
    """Function that greets a person."""
    for x in range(count):
        click.echo(f"{x}. Hello {name}!")


@cli.command()
def com():
    """Function that returns True."""
    click.echo("This is the com function of the cryp2bot module.")
    return True

@cli.command()
def cryp2bot():
    """Function that returns True."""
    click.echo("This is the cryp2bot function of the cryp2bot module. :-)))))")


def usecryp2bot(a, b):
    """Function that returns True."""
    click.echo("This is the testtest function of the cryp2bot module.")
    click.echo(f"Calling the usebitget function from the bitget module with a={a} and b={b}")
    return usebitget(a, b)


if __name__ == "__main__":
    click.echo(click.style("Hello, I am the cryp2 bot", fg="green"))
    cli() # Call the main function
