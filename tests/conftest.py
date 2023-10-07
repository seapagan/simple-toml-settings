"""Configure pytest for the tests in this directory."""
from pathlib import Path

import pytest

from simple_toml_settings.settings import Settings


class TestSettings(Settings):
    """Define a class for testing the Settings class."""

    test_string_var: str = "test_value"
    test_int_var: int = 42


@pytest.fixture()
def settings(fs):
    """Return a Settings object for testing.

    This fixture creates a fake home directory and a fake settings file
    in a virtual filesystem. It then creates a Settings object for the
    test and returns it.
    """
    # Create a fake home directory for the test
    fs.create_dir(Path.home())

    # Create a Settings object for the test
    settings = TestSettings("test_app")
    settings.settings_folder = Path.home() / "test_app"

    return settings
