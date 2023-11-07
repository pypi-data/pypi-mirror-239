from dataclasses import dataclass
from pathlib import Path
from importlib import import_module
import re

from pyrecipes.utils import clean_text, extract_leading_numbers


@dataclass
class SearchMatch:
    line_number: int
    line_text: str
    chapter: int
    recipe_number: int
    recipe_name: str


class Recipe:
    module = "example"

    def __init__(self, recipe_dir: Path):
        self.recipe_dir = recipe_dir
        self.path = recipe_dir / f"{self.module}.py"

    @property
    def package(self):
        if self.exists():
            result = self.path.parent.parent.parent.stem
            if not result.startswith("pyrecipes"):
                return f"pyrecipes.{result}"
            return result

    @property
    def chapter_name(self):
        return self.recipe_dir.parent.stem

    @property
    def name(self):
        return self.recipe_dir.stem

    @property
    def clean_name(self):
        return clean_text(self.name)

    @property
    def number(self):
        return extract_leading_numbers(self.name)

    @property
    def chapter(self):
        return extract_leading_numbers((self.chapter_name))

    def exists(self):
        return self.path.exists()

    def get_module(self):
        if not self.exists():
            raise ModuleNotFoundError(f"This recipe couldn't be found:\n  {self.path}")
        return import_module(
            f"{self.package}.{self.chapter_name}.{self.name}.{self.module}"
        )

    def get_docstring(self):
        return self.get_module().__doc__.replace("\n", " ")

    def get_code(self):
        return self.path.read_text()

    def run(self):
        if self.exists():
            print(f"Running {self.chapter}.{self.number} \n")
            getattr(self.get_module(), "main")()
            print()
        else:
            print(f"Couldn't find Recipe {self.name}")

    def search(self, pattern):
        results = []

        with self.path.open() as file:
            for i, line in enumerate(file, start=1):
                if re.findall(re.compile(pattern), line):
                    results.append(
                        SearchMatch(i, line, self.chapter, self.number, self.clean_name)
                    )
        return results

    def __repr__(self):
        return f"{self.__class__.__name__}({self.path})"

    def __str__(self) -> str:
        return clean_text(self.name)
