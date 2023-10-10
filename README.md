# Simple TOML Settings <!-- omit in toc -->

[![PyPI version](https://badge.fury.io/py/simple-toml-settings.svg)](https://badge.fury.io/py/simple-toml-settings)
[![Tests](https://github.com/seapagan/simple-toml-settings/actions/workflows/tests.yml/badge.svg)](https://github.com/seapagan/simple-toml-settings/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/seapagan/simple-toml-settings/graph/badge.svg?token=6QMS12107L)](https://codecov.io/gh/seapagan/simple-toml-settings)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b8793a3d6eb04167b9e2b13e11f1f12d)](https://app.codacy.com/gh/seapagan/simple-toml-settings/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![CodeQL](https://github.com/seapagan/simple-toml-settings/actions/workflows/codeql.yml/badge.svg)](https://github.com/seapagan/simple-toml-settings/actions/workflows/codeql.yml)

A Python library to save your settings in a TOML file.

- [Development software](#development-software)
- [Installation](#installation)
- [Usage](#usage)
  - [Setup](#setup)
  - [Using the settings](#using-the-settings)
- [Development setup](#development-setup)
  - [Task Runner](#task-runner)
  - [Linting](#linting)
  - [Pre-commit](#pre-commit)
- [License](#license)
- [Credits](#credits)

## Development software

Note that this library is still in the early stages of development and may
contain bugs and/or change in the future.  Please report any bugs you find on
the [issue tracker](https://github.com/seapagan/simple-toml-settings/issues) and
feel free to make suggestions for improvements.

## Installation

You should install this package into a virtual environment.  You can use
[Poetry](https://python-poetry.org/) to do this:

```console
$ poetry add simple-toml-settings
```

If you don't want to use Poetry, you can use pip:

```console
$ pip install simple-toml-settings
```

## Usage

This is a library to save your settings in a TOML file.  It is designed to be
simple to use and to be able to save and load settings from a TOML file with a
minimal of configuration.

For full documentation, see the [documentation site](https://seapagan.github.io/simple-toml-settings/).

Usage is simple:

### Setup

```python
from simple_toml_settings import Settings

class MySettings(Settings):
    """My settings class."""

    # Define the settings you want to save
    name: str = "My Name"
    age: int = 42
    favourite_colour: str = "blue"
    favourite_number: int = 42
    favourite_foods: list = ["pizza", "chocolate", "ice cream"]


settings = MySettings("test_app")
```

The above will automatically create a TOML file in the user's home directory
called `config.toml` and save the settings to it. If the file already exists,
the settings will be loaded from it.

The file contents for the above example would be:

```toml
[test_app]
age = 42
favourite_colour = "blue"
favourite_number = 42
name = "My Name"
schema_version = "none"
favourite_foods = ["pizza", "chocolate", "ice cream"]
```

### Using the settings

Once you have created your settings class, you can use it like any other class:

```python
settings = MySettings("test_app")
settings.favourite_colour = "red"
settings.save()
```

**Note that the current library access methods are not set in stone and may
change in the future.** We will try to keep the changes to a minimum and will
provide a migration path (and backwards compatibility) if we do change them.

## Development setup

Install the dependencies using Poetry:

```console
$ poetry install
```

Then, activate the virtual environment:

```console
$ poetry shell
```

Now, you can start to develop the app.

### Task Runner

The task-runner [Poe the Poet](https://github.com/nat-n/poethepoet) is installed
as a development dependency which allows us to run simple tasks (similar to npm
`scripts`).

These are run (from within the virtual environment) using the `poe` command and
then the script name, for example:

```console
$ poe pre
```

You can define your own, but there are 7 specific ones provided with the script.

- `pre` : Run `pre-commit run --all-files`
- `pylint`: Run Pylint on all Python files in the project.
- `mypy` = Run MyPy type-checker on all Python files in the project.
- `flake8` = Run Flake8 linter on all Python files in the project.
- `black` = Run Black code formatter on all Python files in the project.
- `try` = Run Tryceratops linter on all Python files in the project.

- `lint` = Runs pylint, mypy, flake8 and black in sequence

These are defined in the `pyproject.toml` file in the `[tool.poe.tasks]`
section. Take a look at this file if you want to add or remove tasks.

### Linting

This project includes [flake8](https://flake8.pycqa.org/en/latest/) (with
several plugins) for linting and
[Black](https://black.readthedocs.io/en/stable/) for formatting.
[Mypy](http://mypy-lang.org/) is installed for type checking.
[isort](https://pycqa.github.io/isort/),[Pylint](https://pylint.org/) and
[tyrceratops](https://github.com/guilatrova/tryceratops) are also installed as
standard.

### Pre-commit

There is a [pre-commit](https://pre-commit.com/) configuration provided to run
some checks on the code before it is committed.  This is a great tool to help
keep your code clean.

To install pre-commit, run the following command from inside your venv:

```console
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

## License

This project is released under the terms of the MIT license.

## Credits

The original Python boilerplate for this package was created using
[Pymaker](https://github.com/seapagan/py-maker) by [Grant
Ramsay (seapagan)](https://github.com/seapagan)
