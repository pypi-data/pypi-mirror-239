import pytest

from pyrecipes.chapter import Chapter
from pyrecipes.recipe import Recipe


@pytest.fixture
def chapter(recipe_root_dir):
    yield Chapter(recipe_root_dir / "01_test_chapter")


def test_Chapter_init(chapter, recipe_root_dir):
    assert chapter.chapter_dir == recipe_root_dir / "01_test_chapter"
    assert chapter.number == 1
    assert chapter.name == "01_test_chapter"
    assert chapter.recipes.keys() == {1, 2, 3}
    assert str(chapter) == " 1) Test Chapter"


def test_Chapter_indexing_found_returns_recipe(chapter):
    recipe = chapter[1]
    assert isinstance(recipe, Recipe)
    assert recipe.number == 1


def test_Chapter_indexing_not_found_returns_None(chapter):
    recipe = chapter[200]
    assert recipe is None


def test_Chapter_iterating(chapter):
    expected_recipe_numbers = [1, 2, 3]
    expected_recipe_names = ["01_test_recipe", "02_test_recipe", "03_test_recipe"]

    for (number, recipe), expected_number, expected_name in zip(
        chapter, expected_recipe_numbers, expected_recipe_names
    ):
        assert number == expected_number
        assert recipe.name == expected_name
