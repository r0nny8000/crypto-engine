"""This is the cryp2bot module."""

import click


@click.group()
def cli():
    """add a group of commands to the command line interface."""
    pass

@cli.command()
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
def hello(count, name):
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
    click.echo("This is the cryp2bot function of the cryp2bot module.")
    return True

if __name__ == "__main__":
    cli() # Call the main function
