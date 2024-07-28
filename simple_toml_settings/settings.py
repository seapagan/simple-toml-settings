"""Control the settings of the project.

Allows reading from a settings file and writing to it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar, TypeVar, cast

import rtoml

from simple_toml_settings.exceptions import (
    SettingsNotFoundError,
    SettingsSchemaError,
)
from simple_toml_settings.xdg_config import xdg_config_home

T = TypeVar("T", bound="TOMLSettings")


@dataclass
class TOMLSettings:
    """The main settings class.

    The only required argument is the app_name, which is used to create the
    settings folder. The settings_folder and settings_file_name are optional and
    will default to the app_name preceded by a '.' and config.toml
    respectively.
    """

    app_name: str
    settings_file_name: str = "config.toml"
    auto_create: bool = True
    local_file: bool = False
    flat_config: bool = False
    xdg_config: bool = False

    # the schema_version is used to track changes to the settings file.
    schema_version: str = "none"

    _instances: ClassVar[dict[type[TOMLSettings], TOMLSettings]] = {}

    _ignored_attrs: set[str] = field(
        default_factory=lambda: {
            "_instances",
            "app_name",
            "settings_folder",
            "settings_file_name",
            "auto_create",
            "local_file",
            "flat_config",
            "xdg_config",
        }
    )

    def __post_init__(self) -> None:
        """Create the settings folder if it doesn't exist."""
        self.settings_folder = self.get_settings_folder()

        self.load()

    def get_settings_folder(self) -> Path:
        """Return the settings folder. If it doesn't exist, create it.

        Take into account the `local_file` and `flat_config` settings.
        Note that `local_file` takes precedence over `flat_config`.
        """
        if self.local_file:
            return Path.cwd()

        if self.flat_config:
            return Path.home()

        settings_folder: Path = Path.home() / f".{self.app_name}"

        if self.xdg_config:
            settings_folder = xdg_config_home() / f"{self.app_name}"
        if not settings_folder.exists():
            settings_folder.mkdir(parents=True)

        return settings_folder

    def __post_create_hook__(self) -> None:
        """Allow further customization after a new settings file is created.

        It is provided so that you can add any additional settings that you
        might need, or get information from the user. The subclass should
        override this method, by default it does nothing.

        The save() method IS called after we run this automatically, it should
        never be called manually.
        """

    @classmethod
    def get_instance(
        cls: type[T],
        app_name: str,
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> T:
        """Class method to get or create the Settings instance.

        This is optional (and experimental), and is provided to allow for a
        singleton pattern in derived classes. It is not required to use this
        class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = cls(app_name, *args, **kwargs)
        return cast(T, cls._instances[cls])

    def get_attrs(self, *, include_none: bool = False) -> dict[str, Any]:
        """Return a dictionary of our setting values.

        Values that are None are EXCLUDED by default, but can be included by
        setting 'include_none' to True.
        """
        return {
            a: getattr(self, a)
            for a in dir(self)
            if not a.startswith("_")
            and a not in self._ignored_attrs
            and not callable(getattr(self, a))
            and (include_none or getattr(self, a) is not None)
        }

    def save(self) -> None:
        """Save the settings to the settings file."""
        rtoml.dump(
            {self.app_name: self.get_attrs()},
            self.settings_folder / self.settings_file_name,
        )

    def load(self) -> None:
        """Load the settings from the settings file."""
        try:
            settings = rtoml.load(
                self.settings_folder / self.settings_file_name
            )
        except FileNotFoundError as exc:
            if self.auto_create:
                self.__post_create_hook__()
                self.save()
            else:
                message = "Cant find a Config File, please create one."
                raise SettingsNotFoundError(message) from exc
            return

        # Check if 'schema_version' is present and matches the required one
        file_schema_version = str(
            settings[self.app_name].get("schema_version", None)
        )
        if file_schema_version.lower() not in {self.schema_version, "none"}:
            raise SettingsSchemaError(
                expected=self.schema_version, found=file_schema_version
            )
        for key, value in settings[self.app_name].items():
            setattr(self, key, value)

    def get(
        self,
        key: str,
    ) -> Any:  # noqa: ANN401
        """Get a setting by key."""
        try:
            return getattr(self, key)
        except AttributeError:
            return None

    def set(
        self,
        key: str,
        value: Any,  # noqa: ANN401
        *,
        autosave: bool = True,
    ) -> None:
        """Set a setting by key and value.

        If autosave is True (the default), the settings will be saved to the
        settings file each time it is called.
        """
        setattr(self, key, value)
        if autosave:
            self.save()

    def list_settings(self) -> dict[str, Any]:
        """Return a dictionary of settings."""
        return self.get_attrs()
