"""Configure pytest for the tests in this directory."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from simple_toml_settings.settings import TOMLSettings

if TYPE_CHECKING:
    from pyfakefs.fake_filesystem import FakeFilesystem


class SettingsExample(TOMLSettings):
    """Define a class for testing the Settings class."""

    test_string_var: str = "test_value"
    test_int_var: int = 42


@pytest.fixture
def settings(fs: FakeFilesystem) -> SettingsExample:
    """Return a Settings object for testing.

    This fixture creates a fake home directory in a virtual filesystem. It then
    creates a Settings object for the test and returns it. This Settings object
    creates a settings file in the fake home directory.
    """
    # Create a fake home directory for the test
    fs.create_dir(Path.home())

    # Create and return a Settings object for the test
    return SettingsExample("test_app")


@pytest.fixture
def flat_settings(fs: FakeFilesystem) -> SettingsExample:
    """Return a Settings object for testing with a flat config."""
    # Create a fake home directory for the test
    fs.create_dir(Path.home())

    # Create and return a Settings object for the test
    return SettingsExample("test_app", flat_config=True)


@pytest.fixture
def xdg_settings(fs: FakeFilesystem) -> SettingsExample:
    """Return a Settings object for testing.

    This fixture creates a fake home directory in a virtual filesystem. It then
    creates a Settings object for the test and returns it. This Settings object
    creates a settings file in the fake home directory.
    """
    # Create a fake home directory for the test
    fs.create_dir(Path.home())

    # Create and return a Settings object for the test
    return SettingsExample("test_app", xdg_config=True)
