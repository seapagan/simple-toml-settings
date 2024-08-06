"""Define exceptions for the simple_toml_settings package."""


class SettingsError(Exception):
    """Base exception for settings errors."""


class SettingsNotFoundError(SettingsError):
    """The Settings file has not been found.

    This will be raised if the settings file is not found and auto_create is
    False.
    """


class SettingsSchemaError(SettingsError):
    """The settings file schema does not match the required level."""

    def __init__(self, expected: str, found: str) -> None:
        """Define a custom response for this Exception."""
        self.expected = expected
        self.found = found
        super().__init__(
            f"Schema version mismatch: Expected {self.expected}, "
            f"found {self.found} in file."
        )


class SettingsMutuallyExclusiveError(SettingsError):
    """Two or more mutually exclusive settings are set to True."""

    def __init__(self, attrs: set[str]) -> None:
        """Define a custom response for this Exception."""
        self.attrs = attrs
        super().__init__(f"Only one of {', '.join(self.attrs)} can be True.")


# temporary alias for backwards compatibility
SettingsNotFound = SettingsNotFoundError
