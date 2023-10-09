# Usage

This library is designed to be simple to use, to save and load settings from a
TOML file with a minimal of configuration.

## Setup

Create a class that inherits from the `TOMLSettings` class and define the
settings you want to save as class attributes:

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
    sub_settings: dict = {
        "sub_setting_1": "sub setting 1 text",
        "sub_setting_2": "sub setting 2 text",
    }

settings = MySettings("my_app_name")
```

!!! warning "Use Type-hinting"

    Always use typing hints for your settings as shown above.  This will allow
    the library to automatically convert the settings to the correct type when
    loading them.

The above will automatically create a sub folder in the user's home directory
called `.my_app_name` and will create a TOML file in it called `config.toml`
containing the default settings. If the file already exists, the settings will
be loaded from it.

The file contents for the above example would be:

```toml
[my_app_name]
age = 42
favourite_colour = "blue"
favourite_number = 42
name = "My Name"
schema_version = "none"
favourite_foods = ["pizza", "chocolate", "ice cream"]

[my_app_name.sub_settings]
sub_setting_1 = "sub setting 1 text"
sub_setting_2 = "sub setting 2 text"
```

The above shows how lists are saved as TOML arrays and dictionaries are saved as
TOML tables.

!!! note "`schema_version` key"

    This is used to track the version of the schema
    used to save the settings.  If you change the settings in your app in such
    a way to make older versions incompatible, you should increment the schema
    version.  At the moment, this is not used for anything, but it will be used
    in the future to detect outdated settings files and to allow automatic
    migration of settings.

By default the `schema_version` is set to `none`.  You can change this by
passing it to the custom class on creation:

```python
settings = MySettings("my_app_name", schema_version="1.0.0")
```

By default, the settings will be saved in a file called `config.toml` in the
user's home directory.  You can change this by passing a different filename on
creation:

```python
settings = MySettings("my_app_name", settings_file_name="my_settings.toml")
```

## Using the settings

Once you have created your settings class, you can use it like any other class:

```python
settings = MySettings("my_app_name")
name = settings.name
settings.name = "My New Name"
```

There are also `get` and `set` methods that can be used to access the settings,
this is the preferred method though both methods are supported:

```python
settings = MySettings("my_app_name")
name = settings.get("name")
settings.set("name", "My New Name")
```

The `get` method will return `None` if the setting does not exist.

The advantage of using the `set` method is that it will automatically save the
changed variable to the config file.  If you use the class attributes directly,
you will need to call the `save` method to save the settings:

```python
settings = MySettings("my_app_name")
settings.name = "My New Name"
settings.save()
```

Finally, you can use the `load` and `save` methods to load and save the settings
manually:

```python
settings = MySettings("my_app_name")
settings.load()
settings.set("name", "My New Name")
settings.save()
```

!!! info "Note"

    The `load()` and `save()` methods are automatically called when the class is
    created and when the `set` method is called respectively.  You should not
    need to call `load()` manually.

!!! warning "Warning"

    The current library access methods are not set in stone and may change in
    the future. We will try to keep the changes to a minimum and will provide a
    migration path (and backwards compatibility) if we do change them.
