# Pyrecipes

![ci workflow](https://github.com/ChrisA87/pyrecipes/actions/workflows/ci.yml/badge.svg)
![coverage-badge](https://raw.githubusercontent.com/ChrisA87/pyrecipes/aa37d4757dd7ecbc0b1f2ec93eeb55165be12307/coverage.svg)

Useful recipes from David Beazley & Brian K. Jones' O'Reilly book [Python Cookbook (3rd edition)](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/).

Original code samples at https://github.com/dabeaz/python-cookbook

This project implements a simple CLI tool to list, run and view recipes.

## Installation

```
pip install pyrecipes
```

---

## Example Usage

### Show recipes help and subcommands
```
recipes
```

### List all chapters
```
recipes chapters
```

### List all recipes
```
recipes ls
```

### List all recipes in a specific chapter
```
recipes ls 1
```

### List all recipes in a specific chapter with a short description
```
recipes ls 1 -d
```

### Show recipe code
```
recipes show 1 3
```

### Run the recipe as a script
```
recipes run 1 3
```

### Search for recipes containing a pattern
```
recipes search 'itertools'
recipes search 'itertools' --color green
```
