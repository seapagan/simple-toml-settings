"""Control the settings of the project.

Allows reading from a settings file and writing to it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Set

import rtoml


@dataclass
class TOMLSettings:
    """The main settings class.

    The only required argument is the app_name, which is used to create the
    settings folder. The settings_folder and settings_file_name are optional and
    will default to the app_name preceeded by a '.' and config.toml
    respectively.
    """

    app_name: str
    settings_file_name: str = "config.toml"

    # the schema_version is used to track changes to the settings file.
    schema_version: str = "none"

    _ignored_attrs: Set[str] = field(
        default_factory=lambda: {
            "app_name",
            "settings_folder",
            "settings_file_name",
        }
    )

    def __post_init__(self) -> None:
        """Create the settings folder if it doesn't exist."""
        self.settings_folder: Path = Path.home() / f".{self.app_name}"
        if not self.settings_folder.exists():
            self.settings_folder.mkdir(parents=False)

        self.load()

    def __post_create_hook__(self) -> None:
        """Allow further customization after a new settings file is created.

        It is provided so that you can add any additional settings that you
        might need, or get information from the user. The subclass should
        override this method, by default it does nothing.

        The save() method IS called after we run this automatically, it should
        never be called manually.
        """
        pass

    def get_attrs(self) -> Dict[str, str]:
        """Return a dictionary of our setting values."""
        return {
            a: getattr(self, a)
            for a in dir(self)
            if not a.startswith("_")
            and a not in self._ignored_attrs
            and not callable(getattr(self, a))
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
        except FileNotFoundError:
            self.__post_create_hook__()
            self.save()
            return

        for key, value in settings[self.app_name].items():
            setattr(self, key, value)

    def get(self, key: str) -> Any:
        """Get a setting by key."""
        try:
            return getattr(self, key)
        except AttributeError:
            return None

    def set(self, key: str, value: str, autosave: bool = True) -> None:
        """Set a setting by key and value.

        If autosave is True (the default), the settings will be saved to the
        settings file each time it is called.
        """
        setattr(self, key, value)
        if autosave:
            self.save()

    def list_settings(self) -> Dict[str, str]:
        """Return a dictionary of settings."""
        return self.get_attrs()
