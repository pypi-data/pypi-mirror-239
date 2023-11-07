import click
from pyrecipes.cookbook import cookbook
from pyrecipes.recipe import Recipe


@click.command()
@click.argument("chapter", type=int)
@click.argument("number", type=int)
def show(chapter, number):
    """Shows a recipe"""
    click.echo(f"Showing recipe {chapter}.{number}")
    recipe = cookbook[chapter][number]
    if isinstance(recipe, Recipe):
        click.echo(recipe.get_code())
