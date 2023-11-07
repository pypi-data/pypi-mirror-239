import pytest
from pyrecipes.cookbook import CookBook


@pytest.fixture
def cookbook(recipe_root_dir):
    yield CookBook(recipe_root_dir)


def test_CookBook_init(cookbook, recipe_root_dir):
    assert cookbook.cookbook_dir == recipe_root_dir
    assert cookbook.chapters.keys() == {1, 2, 3}


def test_CookBook_get_recipes_by_chapter__single(cookbook):
    chapter = cookbook.get_chapters(1)
    print(chapter)
    assert len(chapter) == 1
    assert chapter[0].number == 1


def test_CookBook_get_recipes_by_chapter__multiple(cookbook):
    chapters = cookbook.get_chapters(1, 2)

    assert len(chapters) == 2
    assert [chapter.number for chapter in chapters] == [1, 2]
