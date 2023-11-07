import click
from pyrecipes.cookbook import cookbook
from pyrecipes.recipe import Recipe


@click.command()
@click.argument("chapter", type=int)
@click.argument("number", type=int)
def run(chapter, number):
    """Runs a recipe"""
    click.echo(f"running recipe {chapter}.{number}")
    recipe = cookbook[chapter][number]
    if isinstance(recipe, Recipe):
        recipe.run()
