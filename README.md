# Simple TOML Settings <!-- omit in toc -->

[![PyPI version](https://badge.fury.io/py/simple-toml-settings.svg)](https://badge.fury.io/py/simple-toml-settings)
[![Tests](https://github.com/seapagan/simple-toml-settings/actions/workflows/tests.yml/badge.svg)](https://github.com/seapagan/simple-toml-settings/actions/workflows/tests.yml)
[![Codacy Coverage](https://app.codacy.com/project/badge/Coverage/b8793a3d6eb04167b9e2b13e11f1f12d)](https://app.codacy.com/gh/seapagan/simple-toml-settings/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b8793a3d6eb04167b9e2b13e11f1f12d)](https://app.codacy.com/gh/seapagan/simple-toml-settings/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![CodeQL](https://github.com/seapagan/simple-toml-settings/actions/workflows/codeql.yml/badge.svg)](https://github.com/seapagan/simple-toml-settings/actions/workflows/codeql.yml)

A Python library to save your settings in a TOML file.

- [Development software](#development-software)
- [Installation](#installation)
- [Usage](#usage)
  - [Setup](#setup)
  - [Using the settings](#using-the-settings)
- [Development setup](#development-setup)
- [License](#license)
- [Credits](#credits)

## Development software

Note that this library is still in development and may contain bugs and/or
change in the future.  Please report any bugs you find on the [issue
tracker](https://github.com/seapagan/simple-toml-settings/issues) and feel free
to make suggestions for improvements.

## Installation

You should install this package into a virtual environment.  You can use
[Poetry](https://python-poetry.org/) to do this:

```console
$ poetry add simple-toml-settings
```

If you don't want to use Poetry, you can use pip from inside your virtual
environment:

```console
$ pip install simple-toml-settings
```

## Usage

This is a library to save your settings in a TOML file.  It is designed to be
simple to use and to be able to save and load settings from a TOML file with a
minimal of configuration.

The below is a minimal example, for full documentation and information on
available options, see the [documentation
site](https://seapagan.github.io/simple-toml-settings/).

Usage is simple:

### Setup

```python
from simple_toml_settings import TOMLSettings

class MySettings(TOMLSettings):
    """My settings class."""

    # Define the settings you want to save
    name: str = "My Name"
    age: int = 42
    favourite_colour: str = "blue"
    favourite_number: int = 42
    favourite_foods: list = ["pizza", "chocolate", "ice cream"]


settings = MySettings("test_app")
```

The above will automatically create a TOML file in the user's **home** directory
called `config.toml`, in the subdirectory `.test_app/`, and save the settings to
it. If the file already exists, the settings will be loaded from it.

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

See the [Contributing Guidelines](CONTRIBUTING.md) for details of how to
contribute to this project and set it up for development.

## License

This project is released under the terms of the MIT license.

## Credits

The original Python boilerplate for this package was created using
[Pymaker](https://github.com/seapagan/py-maker) by [Grant
Ramsay (seapagan)](https://github.com/seapagan) (Me!! 😄).
