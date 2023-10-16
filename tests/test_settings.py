"""Test the settings module."""
from pathlib import Path

import pytest

from simple_toml_settings.exceptions import SettingsNotFound
from simple_toml_settings.settings import TOMLSettings


def test_config_file_auto_created(settings):
    assert settings.settings_folder.exists()
    assert settings.settings_folder.is_dir()
    assert settings.settings_folder.name == ".test_app"
    assert settings.settings_file_name == "config.toml"


def test_exception_raised_on_missing_config_if_auto_create_is_false(fs):
    """Test that the settings file is not created if auto_create is False."""
    fs.create_dir(Path.home())

    with pytest.raises(SettingsNotFound):
        TOMLSettings("test_app", auto_create=False)


def test_post_create_hook_is_called(fs, mocker):
    """Test that the post_create_hook is called after settings file created."""
    fs.create_dir(Path.home())

    mocker.patch.object(TOMLSettings, "__post_create_hook__")
    settings = TOMLSettings("test_app")

    assert settings.__post_create_hook__.called


def test_get_attrs(settings):
    """Test that we can get the attributes of the settings object."""
    attrs = settings.get_attrs()
    assert attrs["schema_version"] == "none"
    assert attrs["test_string_var"] == "test_value"
    assert attrs["test_int_var"] == 42


def test_get(settings):
    """Test we can get settings."""
    assert settings.get("app_name") == "test_app"
    assert settings.get("nonexistent_key") is None
    assert settings.get("test_string_var") == "test_value"
    assert settings.get("test_int_var") == 42


def test_set(settings):
    """Test that a setting can be set."""
    settings.set("app_name", "new_test_app")
    assert settings.get("app_name") == "new_test_app"


def test_add_and_list_setting(settings):
    """Add a new setting and list all settings."""
    settings.set("new_key", "new_value")
    settings_dict = settings.list_settings()
    assert settings_dict["new_key"] == "new_value"


def test_load_settings(settings):
    """Test that settings are loaded from the settings file."""
    settings.load()
    # length is 3 because of the 'schema' setting
    assert len(settings.list_settings()) == 3

    assert settings.get("schema_version") == "none"
    assert settings.list_settings()["test_string_var"] == "test_value"
    assert settings.list_settings()["test_int_var"] == 42


def test_set_schema_version(settings):
    """Test that the schema_version can be set using the 'set' method."""
    settings.set("schema_version", "1.0.0")
    settings.load()
    assert settings.get("schema_version") == "1.0.0"


def test_autosave(settings):
    """Test that settings are auto saved when autosave is True."""
    settings.set("test_string_var", "new_value")
    settings.load()
    assert settings.get("test_string_var") == "new_value"


def test_no_autosave(settings):
    """Test that settings are not auto saved when autosave is False."""
    settings.set("test_string_var", "new_value", autosave=False)
    settings.load()
    assert settings.get("test_string_var") == "test_value"


def test_custom_file_name(fs):
    """Test that the settings file name can be customized."""
    custom_file_name = "custom_config.toml"

    fs.create_dir(Path.home())
    settings = TOMLSettings("test_app", settings_file_name=custom_file_name)

    assert (Path.home() / ".test_app" / custom_file_name).exists()

    assert settings.settings_file_name == custom_file_name
    assert settings.settings_folder.name == ".test_app"
    assert settings.settings_folder / settings.settings_file_name


def test_items_on_ignored_attrs(settings):
    """Test that the ignored attributes are not returned by items()."""
    list_settings = settings.list_settings()

    for setting in settings._ignored_attrs:
        assert setting not in list_settings
