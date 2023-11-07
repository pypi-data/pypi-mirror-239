from pathlib import Path

from pyrecipes import COOKBOOK_DIR
from pyrecipes.chapter import Chapter


class CookBook:
    def __init__(self, cookbook_dir: Path = COOKBOOK_DIR) -> None:
        self.cookbook_dir = cookbook_dir
        self.chapters: dict[int, Chapter] = {}
        self._collect()

    def _collect(self):
        """Collects all chapters in cookbok_dir"""
        for chapter_dir in sorted(self.cookbook_dir.glob("[0-9]*")):
            chapter = Chapter(chapter_dir)
            self.chapters[chapter.number] = chapter

    def get_chapters(self, *numbers: int):
        return [self.chapters.get(number) for number in numbers]

    def __getitem__(self, key):
        return self.chapters.get(key)

    def __iter__(self):
        for key, value in self.chapters.items():
            yield key, value


cookbook = CookBook(COOKBOOK_DIR)
