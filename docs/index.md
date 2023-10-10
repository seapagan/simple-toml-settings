# Simple TOML Settings <!-- omit in toc -->

[![PyPI version](https://badge.fury.io/py/simple-toml-settings.svg)](https://badge.fury.io/py/simple-toml-settings)&nbsp;
[![Tests](https://github.com/seapagan/simple-toml-settings/actions/workflows/tests.yml/badge.svg)](https://github.com/seapagan/simple-toml-settings/actions/workflows/tests.yml)&nbsp;
[![codecov](https://codecov.io/gh/seapagan/simple-toml-settings/graph/badge.svg?token=6QMS12107L)](https://codecov.io/gh/seapagan/simple-toml-settings)&nbsp;
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b8793a3d6eb04167b9e2b13e11f1f12d)](https://app.codacy.com/gh/seapagan/simple-toml-settings/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)&nbsp;
[![CodeQL](https://github.com/seapagan/simple-toml-settings/actions/workflows/codeql.yml/badge.svg)](https://github.com/seapagan/simple-toml-settings/actions/workflows/codeql.yml)

A Python library to save your settings in a TOML file.

!!! danger "Development software"

    Note that this library is still in the early stages of development and may
    contain bugs and/or change in the future.  Please report any bugs you find
    on the [issue tracker](https://github.com/seapagan/simple-toml-settings/issues){:target="_blank"}
    and feel free to make suggestions for improvements.

---

A quick example:

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


settings = MySettings("my_app_name")
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

---
Once you have created your settings class, you can use it like any other class:

```python
settings = MySettings("my_app_name")
name = settings.name
settings.favourite_colour = "red"
settings.save()
```

See the rest of the documentation for more details.
