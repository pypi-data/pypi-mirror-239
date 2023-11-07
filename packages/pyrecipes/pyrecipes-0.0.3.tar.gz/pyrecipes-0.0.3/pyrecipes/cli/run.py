import click
from pyrecipes.cookbook import cookbook
from pyrecipes.recipe import Recipe


@click.command()
@click.argument("chapter", type=int)
@click.argument("number", type=int)
def run(chapter, number):
    """Runs a recipe"""
    recipe = cookbook[chapter][number]
    if isinstance(recipe, Recipe) and recipe.exists():
        recipe.run()
    else:
        click.echo(f"Couldn't find recipe {chapter}.{number}")
