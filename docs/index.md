# Simple TOML Settings <!-- omit in toc -->

[![PyPI version](https://badge.fury.io/py/simple-toml-settings.svg)](https://badge.fury.io/py/simple-toml-settings)&nbsp;
[![Test Suite](https://github.com/seapagan/simple-toml-settings/actions/workflows/testing.yml/badge.svg)](https://github.com/seapagan/simple-toml-settings/actions/workflows/testing.yml)&nbsp;
[![codecov](https://codecov.io/gh/seapagan/simple-toml-settings/graph/badge.svg?token=6QMS12107L)](https://codecov.io/gh/seapagan/simple-toml-settings)&nbsp;
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b8793a3d6eb04167b9e2b13e11f1f12d)](https://app.codacy.com/gh/seapagan/simple-toml-settings/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)&nbsp;
[![CodeQL](https://github.com/seapagan/simple-toml-settings/actions/workflows/codeql.yml/badge.svg)](https://github.com/seapagan/simple-toml-settings/actions/workflows/codeql.yml)

A Python library to save your settings in a TOML file.

!!! info "Package Status"

    Note that there is still additional functionality planned to be added to
    this package, but the methodology is to keep the package simple to use and
    understand. Any additional functionality will be added in a way that is
    backward compatible and optional.

    The package is considered stable and is being used in production in several
    non-trivial applications. Any security issues or bugs will be fixed as soon
    as reported.

    Please report any bugs you find on the
    [issue tracker](https://github.com/seapagan/simple-toml-settings/issues) and
    feel free to make suggestions for improvements.

---

## Features

- Transparently save and load settings to and from a TOML file, using a simple
  class definition.
- Automatically create a folder in the user's home directory to store the
  settings, write directly to the home folder, or use the application's local
  directory.
- Option to use the `XDG_CONFIG_HOME` environment variable to store the settings
  in the `XDG` configuration directory, or default to `XDG` method of storing
  configuration files in the `~/.config/<app_name` folder if this is not set.
- By default the setting file is automatically created when the class is
  instantiated and the settings are saved to it. If the file already exists, the
  settings are loaded from it instead. This can be disabled if required.
- Allows to run WITHOUT a settings file, so you can use the settings class
  without needing to save the settings. This way all the defaults are used, and
  then the user can manually create the settings file if they want to change the
  defaults.
- The settings filename is configurable or defaults to `config.toml`.
- Provides a hook to run code when the setting file is first created, so you can
  perform any initialisation required.
- Provides a `get_instance` method to get a single instance of the settings
  class, so you can use the same settings throughout your application. You can
  still create an instance directly if desired.
- Full test suite with 100% coverage.
- Supports Python 3.9 and above.
- Maintained and updated regularly with new features and bug fixes.

## A Quick Example

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

The above will automatically create a `Folder` in the users home directory
called `.test_app`, a configuration file in this called `config.toml` and then
save the default settings to it.

However, if the file already exists, the settings will be loaded from it.

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
settings = MySettings("test_app")
settings.favourite_colour = "red"
settings.save()
```

See the rest of the documentation for more details.
