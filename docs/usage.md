# Usage

This library is designed to be simple to use, to save and load settings from a
TOML file with a minimal of configuration.

!!! warning "Warning"

    The current library access methods are not set in stone and may change in
    the future. We will try to keep the changes to a minimum and will provide a
    migration path (and backwards compatibility) if we do change them.

## Setup

Create a class that inherits from the `TOMLSettings` class and define the
settings you want to save as class attributes:

```python
from simple_toml_settings import TOMLSettings

class MySettings(TOMLSettings):
    """My settings class."""

    # Define the settings you want to save
    name: str = "My Name"
    age: int = 53
    favourite_colour: str = "blue"
    favourite_number: int = 42
    favourite_foods: list = ["pizza", "chocolate", "ice cream"]
    sub_settings: dict = {
        "sub_setting_1": "sub setting 1 text",
        "sub_setting_2": "sub setting 2 text",
    }
```

!!! warning "Use Type-hinting"

    Always use typing hints for your settings as shown above.  This will allow
    the library to automatically convert the settings to the correct type when
    loading them.

You can now create an instance of your settings class and use it to save and
load settings:

```python
settings = MySettings("my_app_name")
```

!!! tip "`get_instance()` method"

    You can also use the `get_instance()` method to create an instance of your
    settings class.  This is useful if you need to use the settings in multiple
    places in your app, as it will return an already existing instance of the
    settings instead of creating a new one. If one does not already exist, it
    will be created and returned.

    ```python
    settings = MySettings.get_instance("my_app_name")
    ```

    This is the preferred method and ensures that the settings class is a
    **Singleton** so you only have one instance of the settings in your app.

The above will automatically create a sub folder in the user's home directory
called `.my_app_name` and will create a TOML file in it called `config.toml`
containing the default settings. If the file already exists, the settings will
be loaded from it.

The file contents for the above example would be:

```toml
[my_app_name]
age = 53
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

!!! note "`schema_version` key [optional]"

    This is used to track the version of the schema
    used to save the settings.  If you change the settings in your app in such
    a way to make older versions incompatible, you should increment the schema
    version.  If the schema version is not set, it will default to `none`.

    The schema is checked when the settings are loaded and if the schema version
    in the file is different to the schema version in the class, an exception
    will be raised (**`simple_toml_settings.exceptions.SettingsSchemaError`**).
    You can catch this exception and handle it as you wish.

    **If the schema version is set to `none` (or missing) in the file, no schema
    checking will be performed and no exception raised.**

By default the `schema_version` is set to `none`.  You can change this by
passing it to the custom class on creation:

```python
settings = MySettings("my_app_name", schema_version="1.0.0")
```

By default, the settings will be saved in a file called `config.toml` in a
subfolder of the user's home directory.  You can change this by passing a
different filename on creation:

```python
settings = MySettings("my_app_name", settings_file_name="my_settings.toml")
```

The subfolder will be created if it does not exist, and is the same as the app
name but with a `.` prepended to it.  So, for the above example, the settings
will be saved as `~/.my_app_name/my_settings.toml`.

!!! note
    In future versions the folder name will be configurable, and the folder itself
    will be optional, so the file can be stored in the user's home folder
    directly.

## Using the settings

!!! danger "`None` values"

    The library does not support saving `None` values.  If you need to save a
    `None` value, you should use a different value (such as an empty string or
    `0`) and convert it to `None` in your app.

    This is because TOML does not support `None` values and the library will
    convert `None` values to `null` when saving the settings.

    We may add support for this in the future, but for now you should avoid
    using `None` values unless they are a default and will never need to be
    saved - **any `None` value will not be saved to the config file**.

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

## Options

There are a couple of options you can pass to the `TOMLSettings` constructor to
change the behaviour of the class:

### `settings_file_name`

This is the name of the settings file to use.  By default this is set to
`config.toml`.

### `auto_create`

This defaults to `True` and will automatically create the settings file if it
does not exist and fill it with the default values.  If set to `False`, the
class will raise an exception
(**`simple_toml_settings.exceptions.SettingsNotFoundError`**) if the settings
file does not exist. You can catch this exception and handle it as you wish.
*The folder will be created anyway if it does not exist, as the assumption is
that you will want to save the settings at some point*.

!!! danger "Deprecation warning"

    The exception was originally called **`SettingsNotFound`** but has been
    renamed to **`SettingsNotFoundError`** to be more consistent with Python
    naming conventions.  The old name still works, but will be removed in a
    future release.

### `local_file`

This defaults to `False` and will cause the settings file to be saved/read from
the current directory instead of the user's home directory.  This is good for
utility apps that need different settings for different projects / filelists.

## Post-create hook

If you need to do some further processing, or set some input from the user after
the new config file has been created (for example to fill in the default values
with some real data), you can override the
`__post_create_hook__()` method in your class:

```python
from simple_toml_settings import TOMLSettings

class MySettings(TOMLSettings):
    """My settings class."""

    # Define the settings you want to save
    name: str = "My Name"
    age: int = 53
    favourite_colour: str = "blue"
    favourite_number: int = 42
    favourite_foods: list = ["pizza", "chocolate", "ice cream"]
    sub_settings: dict = {
        "sub_setting_1": "sub setting 1 text",
        "sub_setting_2": "sub setting 2 text",
    }

    def __post_create_hook__(self):
        """Post create hook."""
        self.name = input("Enter your name: ")
        self.age = int(input("Enter your age: "))
        self.favourite_colour = input("Enter your favourite colour: ")
        self.favourite_number = int(input("Enter your favourite number: "))
```

!!! info "Note"

    This is a special method that is called automatically after the config file
    has been created.  It is not a normal method and **should not be called
    directly**. It is **NOT** called when an existing config file is loaded.

    The `save()` method will be called automatically after the hook has been
    executed. There is no need to call the `super()` method in your hook since
    it is just a placeholder method.
