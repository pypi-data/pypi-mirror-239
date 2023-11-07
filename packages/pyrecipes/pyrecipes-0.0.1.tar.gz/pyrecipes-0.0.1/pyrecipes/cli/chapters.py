import click
from pyrecipes.cookbook import cookbook


@click.command()
def chapters():
    """List chapters"""
    for _, chapter in cookbook:
        click.echo(chapter)
