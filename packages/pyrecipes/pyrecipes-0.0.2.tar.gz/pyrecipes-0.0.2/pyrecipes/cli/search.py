import click
import re
from colorama import Fore, init
from pyrecipes.cookbook import cookbook
from pyrecipes.recipe import SearchMatch

init(autoreset=True)

COLOURS = {
    "black": Fore.BLACK,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
    "none": Fore.RESET,
}


def render_match(pattern: str, match: SearchMatch, color=Fore.RED):
    click.echo(
        f"Recipe: {match.chapter}.{match.recipe_number}, Line: {match.line_number} - {match.recipe_name}"
    )
    click.echo(
        re.sub(
            re.compile(pattern), color + pattern + Fore.RESET, match.line_text
        ).lstrip()
    )


@click.command()
@click.argument("pattern", type=str)
@click.option(
    "-c",
    "--color",
    type=click.Choice(COLOURS.keys(), case_sensitive=False),
    default="red",
)
def search(pattern, color):
    """Search the recipes for a pattern"""
    for _, chapter in cookbook:
        for _, recipe in chapter:
            matches = recipe.search(pattern)
            if matches:
                for match in matches:
                    render_match(pattern, match, COLOURS.get(color.lower(), "red"))
