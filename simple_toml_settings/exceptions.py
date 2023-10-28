"""Define exceptions for the simple_toml_settings package."""


class SettingsError(Exception):
    """Base exception for settings errors."""


class SettingsNotFoundError(SettingsError):
    """The Settings file has not been found.

    This will be raised if the settings file is not found and auto_create is
    False.
    """
