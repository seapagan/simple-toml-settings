# Usage

This library is designed to be simple to use, to save and load settings from a
TOML file with a minimal of configuration.

*This is currently a basic description of how to use the library and will be
improved very shortly.*

Usage is simple:

## Setup

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

Note the `schema_version` key.  This is used to track the version of the schema
used to save the settings.  If you change the settings in your app, you should
increment the schema version.  This will cause the settings to be re-saved with
the new schema version. At the moment, this is not used for anything, but it
wil be used in the fiture to detect outdated settings files and to allow
automatic migration of settings.

By default the `schema_version` is set to `none`.  You can change this by
setting the `schema_version` class attribute in your settings class:

```python
class MySettings(Settings):
    """My settings class."""

    schema_version: str = "1.0.0"
```

or by passing it to the `Settings` class:

```python
settings = MySettings("my_app_name", schema_version="1.0.0")
```

By default, the settings will be saved in a file called `config.toml` in the
user's home directory.  You can change this by passing a different filename to
the `Settings` class:

```python
settings = MySettings("my_app_name", "my_settings.toml")
```

The former version is recommended.

## Using the settings

Once you have created your settings class, you can use it like any other class:

```python
settings = MySettings("my_app_name")
name = settings.name
```

**Note that the current library access methods are not set in stone and may
change in the future.** We will try to keep the changes to a minimum and will
provide a migration path (and backwards compatibility) if we do change them.
