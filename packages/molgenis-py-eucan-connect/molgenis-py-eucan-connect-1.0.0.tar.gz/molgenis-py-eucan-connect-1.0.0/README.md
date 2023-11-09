# molgenis-py-eucan-connect

MOLGENIS Python tooling for the EUCAN-Connect Catalogue.

## Description
This library contains tools for the MOLGENIS EUCAN-Connect Catalogue that help with
integrating data from external catalogues. For example BirthCohorts and Maelstrom.

## Usage

These tools can be used as a library in a script.
Start by installing the library with `pip install molgenis-py-eucan-connect`.

For an example of how to use this library to stage and publish nodes, see [`example.py`](scripts/example.py).

## For developers
This project uses [pre-commit](https://pre-commit.com/) and [pipenv](https://pypi.org/project/pipenv/)
for the development workflow.

Install pre-commit and pipenv if you haven't already:
```
pip install pre-commit
pip install pipenv
```

Clone or check out this repository with git and install the git commit hooks:
```
pre-commit install
```

Create an environment and install the package including all (dev) dependencies:
```
pipenv install --dev
```

Activate the virtual environment:
```
pipenv shell
```

Build and run the tests:
```
tox
```

>Note: If you want automatic code formatting in your IDE, you need to configure file watchers
  for `black` (the code formatter) and `isort` (the formatter for import statements). Here
  are some examples of how to configure them in `PyCharm`:
>
> ![img.png](.img/example_black_config.png)
> ![img_1.png](.img/example_isort_config.png)
