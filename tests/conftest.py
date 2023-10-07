"""Configure pytest for the tests in this directory."""
from pathlib import Path

import pytest

from simple_toml_settings.settings import Settings


@pytest.fixture()
def settings(fs):
    """Return a Settings object for testing.

    This fixture creates a fake home directory and a fake settings file
    in a virtual filesystem. It then creates a Settings object for the
    test and returns it.
    """
    # Create a fake home directory for the test
    fs.create_dir(Path.home())

    # Create a fake settings file
    fs.create_file(
        Path.home() / "test_app" / "config.toml",
        contents="[test_app]\napp_name = 'test_app'\n",
    )

    # Create a Settings object for the test
    settings = Settings("test_app")
    settings.settings_folder = Path.home() / "test_app"

    return settings
