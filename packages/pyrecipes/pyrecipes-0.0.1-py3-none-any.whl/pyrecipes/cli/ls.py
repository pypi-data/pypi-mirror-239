import click
from pyrecipes.chapter import Chapter
from pyrecipes.cookbook import cookbook


def render_chapter(chapter: Chapter, describe: bool = False):
    width = len(str(chapter)) + 2
    click.echo(f'{"=" * width}\n{str(chapter):^{width}}\n{"=" * width}')
    for _, recipe in chapter:
        click.echo(f"  {recipe}")
        if describe:
            click.echo(f"    {recipe.get_docstring()}\n")
    click.echo("")


@click.command()
@click.option(
    "-d",
    "--describe",
    is_flag=True,
    help="Shows descriptions of the recipes",
)
@click.argument("chapter", required=False, default=None, type=int)
def ls(chapter, describe):
    """List recipes

    \b
    The default behaviour lists the titles of all recipes for all chapters.
    Limit the output to a specific recipe by adding an additional 'CHAPTER'
    argument e.g. to list chapter 1 recipes

    \b
        recipes ls 1

    You can also add a '-d' flag to display a short description of each recipe.
    """

    if chapter:
        render_chapter(cookbook[chapter], describe)
    else:
        for _, chapter in cookbook:
            render_chapter((chapter), describe)
